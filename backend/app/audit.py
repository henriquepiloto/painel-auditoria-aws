from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from app.assume_role import assume_role
from app.utils import make_creds_dict, check_iam
from app.auth import get_current_user  # Importa a proteção JWT
from app.database import SessionLocal, AuditLog  # Importa conexão e modelo
import pandas as pd
import datetime
import boto3
from io import BytesIO
import os

router = APIRouter()

class RoleRequest(BaseModel):
    account_id: str
    role_name: str
    session_name: str
    cliente: str

@router.post("/analisar")
def run_auditoria(
    request: RoleRequest,
    download: bool = Query(False),
    user: dict = Depends(get_current_user)  # Protege a rota com autenticação
):
    try:
        # Assume Role
        creds_raw = assume_role(request.account_id, request.role_name, request.session_name)
        creds = make_creds_dict(creds_raw)

        # Executa a auditoria
        findings = check_iam(creds, request.cliente, request.account_id)

        if not findings:
            return {"status": "ok", "mensagem": "Nenhum problema identificado"}

        # Salva no banco de dados
        db = SessionLocal()
        for item in findings:
            log = AuditLog(
                cliente=item.get("Conta"),
                account_id=item.get("ID da Conta"),
                servico=item.get("Serviço"),
                descricao=item.get("Descrição"),
                motivo=item.get("Motivo"),
                severidade=item.get("Severidade"),
                recomendacao=item.get("Recomendacao de solucao"),
            )
            db.add(log)
        db.commit()
        db.close()

        # Gera o dataframe
        df = pd.DataFrame(findings)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"relatorio_{request.cliente}_{timestamp}.xlsx"

        if download:
            # Upload para o bucket S3
            bucket_name = os.getenv("S3_BUCKET", "audit-report-bucket-select")
            file_stream = BytesIO()
            df.to_excel(file_stream, index=False, engine='openpyxl')
            file_stream.seek(0)

            s3 = boto3.client("s3")
            s3.upload_fileobj(file_stream, bucket_name, filename)

            url = f"https://{bucket_name}.s3.amazonaws.com/{filename}"
            return {
                "status": "ok",
                "download_url": url,
                "itens_encontrados": len(findings)
            }

        else:
            return {
                "status": "ok",
                "itens_encontrados": len(findings),
                "dados": findings
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/relatorios")
def listar_relatorios(user: dict = Depends(get_current_user)):
    try:
        db = SessionLocal()
        logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()
        db.close()

        resultado = [
            {
                "cliente": log.cliente,
                "account_id": log.account_id,
                "servico": log.servico,
                "descricao": log.descricao,
                "motivo": log.motivo,
                "severidade": log.severidade,
                "recomendacao": log.recomendacao,
                "timestamp": log.timestamp.isoformat()
            } for log in logs
        ]

        return {"status": "ok", "relatorios": resultado}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

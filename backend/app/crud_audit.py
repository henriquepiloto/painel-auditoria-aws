from sqlalchemy.orm import Session
from models import AuditLog

def salvar_findings_no_banco(findings: list, db: Session):
    for item in findings:
        log = AuditLog(
            cliente=item["Conta"],
            account_id=item["ID da Conta"],
            servico=item["Serviço"],
            descricao=item["Descrição"],
            motivo=item["Motivo"],
            severidade=item["Severidade"],
            recomendacao=item["Recomendacao de solucao"]
        )
        db.add(log)
    db.commit()

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, index=True)
    account_id = Column(String, index=True)
    servico = Column(String)
    descricao = Column(String)
    motivo = Column(String)
    severidade = Column(String)
    recomendacao = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Configuração do banco de dados PostgreSQL AWS
DATABASE_URL = "postgres://auditor:RbxZm079_Gg!@audit-db.chmznmevttks.us-east-1.rds.amazonaws.com:5432/auditdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
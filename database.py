from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from typing import Generator
# O 'from models import Stock' não é mais necessário aqui.

# Configuração da Conexão
engine = create_engine("sqlite:///stock.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Renomeei 'session' para 'SessionLocal' para evitar confusão com 'Session' do SQLAlchemy

class Base(DeclarativeBase):
    pass
import models

Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
    """Dependency para obter a sessão do banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
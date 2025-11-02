# Arquivo: test_main.py
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from models import Stock # Importe o modelo para criar a tabela de teste

# --- Princípio de Design: Isolação de Testes (Test Driven Development - TDD) ---
# Em testes de banco de dados, é crucial usar um banco de dados de teste isolado
# e temporário (ex: 'sqlite:///./test.db') para que os testes não interfiram
# no seu banco de dados de desenvolvimento ('sqlite://stock.db').

# Configuração do Banco de Dados de Teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" # Banco de teste isolado
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Configura o TestClient
client = TestClient(app)

# 1. Função para sobrescrever a dependência de banco de dados
def override_get_db():
    """Gera uma sessão para o banco de dados de teste."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Sobrescreve a dependência
app.dependency_overrides[get_db] = override_get_db

# 2. Fixture para garantir um banco limpo antes de cada teste
# O '@pytest.fixture' garante que essa função rode antes e depois de cada teste
def setup_teardown():
    # SETUP: Cria todas as tabelas no banco de teste antes do teste
    Base.metadata.create_all(bind=engine)
    yield
    # TEARDOWN: Remove todas as tabelas após o teste (limpeza)
    Base.metadata.drop_all(bind=engine)

# 3. O Teste Unitário da Rota POST
def test_create_stock(setup_teardown):
    # Dados que serão enviados na requisição POST
    stock_data = {
        "symbol": "PYTH",
        "name": "Pythia Analytics",
        "current_price": 42.42
    }
    
    # Simula a requisição POST
    response = client.post("/stocks", json=stock_data)
    
    # --- Assertions (Verificações) ---
    # 1. Verifica se o status code é o esperado (201 CREATED)
    assert response.status_code == 201
    
    # 2. Verifica se o JSON de resposta contém os dados enviados + o 'id'
    data = response.json()
    assert data["symbol"] == "PYTH"
    assert data["name"] == "Pythia Analytics"
    assert data["current_price"] == 42.42
    assert "id" in data # Verifica se o ID foi gerado pelo banco
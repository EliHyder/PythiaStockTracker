# Arquivo: repository.py
import pandas as pd
from typing import List, Optional
from sqlalchemy.orm import Session
from models import Stock
from schemas import StockCreate
import numpy as np

# --- Princípio de Design: Padrão Repository (Isolamento da Persistência) ---
# A responsabilidade de manipular os dados (CRUD) está aqui.
# Isso torna a lógica de persistência fácil de trocar (ex: de SQL para NoSQL)
# sem impactar o resto da aplicação.

def add_stock(db: Session, stock: StockCreate) -> Stock:
    """Adiciona uma nova ação ao banco de dados."""
    stock_data = stock.model_dump()
    stock_db = Stock(**stock_data)

    db.add(stock_db)
    db.commit()
    db.refresh(stock_db)
    return stock_db

def get_stocks(db: Session, skip: int = 0, limit: int = 10) -> List[Stock]:
    """Busca ações com paginação (offset e limit)."""
    consulta = db.query(Stock).offset(skip).limit(limit)
    return consulta.all()

def calculate_average_price(db: Session) -> float:
    """Calcula o preço médio de todas as ações."""
   
    lista_de_stocks = get_stocks(db, limit=None) # Busca todos os stocks para o cálculo
    
    if not lista_de_stocks:
        return 0.0
        
    df = pd.DataFrame([stock.__dict__ for stock in lista_de_stocks])
    return df["current_price"].mean()

def get_stock_by_id(stock_id: int, db: Session) -> Optional[Stock]:
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    return stock

def delete_stock_by_id(stock_id: int, db: Session) -> bool:
    row = db.query(Stock).filter(Stock.id == stock_id).delete(synchronize_session=False)
    db.commit()
    return row > 0

def calculate_volatility(stock_id: int, db: Session) -> Optional[dict]:
    """Calcula a volatilidade (desvio padrão simulado) para uma ação."""
    
    # 1. Busca a ação para obter o símbolo.
    stock = get_stock_by_id(stock_id, db)
    if not stock:
        return None
        
    # --- Princípio de Design: Simulação de Dados para Análise (Contexto Data Science) ---
    # Para calcular volatilidade (desvio padrão), você precisa de uma série de preços.
    # Vamos simular 10 "preços históricos" em torno do preço atual.
    current_price = stock.current_price
    
    # Cria 10 preços aleatórios com uma pequena variação em torno do preço atual
    # np.random.normal(média, desvio_padrão_da_distribuição, número_de_pontos)
    simulated_prices = np.random.normal(loc=current_price, scale=1.5, size=10)
    
    # 2. Calcula a Volatilidade (Desvio Padrão)
    volatility = np.std(simulated_prices)
    
    return {
        "stock_id": stock.id,
        "symbol": stock.symbol,
        "volatility": float(volatility) # numpy float para float nativo do Python
    }
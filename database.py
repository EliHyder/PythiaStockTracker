from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from typing import Generator, List

from schemas import StockCreate
import pandas as pd

engine = create_engine("sqlite:///stock.db")
session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

from models import Stock

Base.metadata.create_all(bind=engine)

def get_db() -> Generator:
    db = session()
    try:
        yield db
    finally:
        db.close()

def get_stocks(db: Session, skip: int = 0, limit: int = 10,) -> List[Stock]:
    stocks = db.query(Stock).offset(skip).limit(limit).all()
    stocks_dict = [stock.__dict__ for stock in stocks]
    print(stocks_dict)
    return stocks_dict

def add_stock(db: Session, stock: StockCreate):
    stock_data = stock.model_dump()
    stock_db = Stock(**stock_data)
    db.add(stock_db)
    db.commit()
    db.refresh(stock_db)
    print(stock_db.__dict__)
    return stock_db

def calculate_average_stocks(db: Session):
    lista_de_stocks = get_stocks(db)
    if not lista_de_stocks: return 0.0

    df = pd.DataFrame([stock.__dict__ for stock in lista_de_stocks])
    return df["current_price"].mean()
    
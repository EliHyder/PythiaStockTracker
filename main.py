from fastapi import FastAPI, Depends, status, HTTPException
import schemas
from database import get_db, add_stock, get_stocks, calculate_average_stocks
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

@app.get("/stocks", response_model=List[schemas.StockResponse], status_code=status.HTTP_200_OK)
def list_stocks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    if limit > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O limite máximo de ações por requisição é 100.")
    return get_stocks(db, skip, limit)

@app.post("/stocks", response_model=schemas.StockResponse, status_code=status.HTTP_201_CREATED)
def create_stocks(stock: schemas.StockCreate, db: Session = Depends(get_db)):
    return add_stock(db, stock)

@app.get("stocks/average", response_model=schemas.StockAnalyzedResponse, status_code=status.HTTP_200_OK)
def get_average_stocks(db: Session = Depends(get_db)):
    media = calculate_average_stocks(db)
    return {"average_price": media}
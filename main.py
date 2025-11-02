from fastapi import FastAPI, Depends, status, HTTPException
import schemas
from database import get_db
from repository import add_stock, get_stocks, calculate_average_price, get_stock_by_id, delete_stock_by_id, calculate_volatility
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

@app.get("/stocks/average", response_model=schemas.Average, status_code=status.HTTP_200_OK)
def get_average_stocks(db: Session = Depends(get_db)):
    media = calculate_average_price(db)
    return {"average_price": media}

@app.get("/stocks/{stock_id}", response_model=schemas.StockResponse, status_code=status.HTTP_200_OK)
def get_stock_by_id_route(stock_id: int, db: Session = Depends(get_db)):
    stock = get_stock_by_id(stock_id, db)
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock Not Found")
    return stock

@app.delete("/stocks/{stock_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stock_by_id_route(stock_id: int, db: Session = Depends(get_db)):
    was_delete = delete_stock_by_id(stock_id, db)
    if not was_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return

@app.get("/stocks/{stock_id}/volatility", response_model=schemas.VolatilityResponse, status_code=status.HTTP_200_OK)
def get_stock_volatility(stock_id: int, db: Session = Depends(get_db)):
    """Retorna a volatilidade simulada de uma ação pelo ID."""
    #Chama o repositório para o cálculo
    analysis_data = calculate_volatility(stock_id=stock_id, db=db)
    
    # Tratamento de erro
    if analysis_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock with ID {stock_id} not found."
        )
        
    return analysis_data
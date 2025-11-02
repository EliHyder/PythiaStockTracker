from pydantic import BaseModel, ConfigDict

class StockBase(BaseModel):
    symbol: str
    name: str
    current_price: float

class StockCreate(StockBase):
    pass

class StockResponse(StockBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Average(BaseModel):
    average_price: float

class VolatilityResponse(BaseModel):
    stock_id: int
    symbol: str
    volatility: float # O desvio padrão simulado
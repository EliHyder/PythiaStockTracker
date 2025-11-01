from pydantic import BaseModel, ConfigDict

class StockBase(BaseModel):
    symbol: str
    name: str
    current_price: float

class StockCreate(StockBase):
    pass

class StockResponse(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Average(BaseModel):
    average_price: float
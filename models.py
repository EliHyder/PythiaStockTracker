from database import Base
from sqlalchemy import Column, Integer, String, Float

class Stock(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True)
    name = Column(String)
    current_price = Column(Float)

    
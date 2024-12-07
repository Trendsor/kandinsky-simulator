from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Create a MetaData instance
metadata = MetaData()

# Create a base class for models
Base = declarative_base(metadata=metadata)

# Define your table models
class StockDataRaw(Base):
    __tablename__ = "stock_data_raw"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(10), nullable=False)
    price = Column(DECIMAL, nullable=False)
    size = Column(Integer, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)

class StockDataProcessed(Base):
    __tablename__ = "stock_data_processed"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(10), nullable=False)
    price = Column(DECIMAL, nullable=False)
    size = Column(Integer, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    rolling_mean_200 = Column(DECIMAL)
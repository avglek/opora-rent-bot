from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import  Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Base(DeclarativeBase): pass

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

class Rent(Base):
    __tablename__="rent"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    img = Column(String)
    price_id = Column(Integer, ForeignKey("price.id"))
    price = relationship("Price", back_populates="rents")

class Price(Base):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(Integer)
    two_week = Column(Integer)
    day = Column(Integer)
    rents = relationship("Rent", back_populates="price")
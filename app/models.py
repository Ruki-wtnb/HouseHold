
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, Date
from .database import Base

from sqlalchemy.ext.declarative import AbstractConcreteBase


class Categories(AbstractConcreteBase, Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    en_name = Column(String(50), nullable=False)

class FixedCostsCategories(Categories):
    __tablename__ = 'fixed_costs_categories'
    __table_args__ = {'extend_existing': True}

class VariableCostsCategories(Categories):
    __tablename__ = 'variable_costs_categories'
    __table_args__ = {'extend_existing': True}


class FixedCosts(Base):
    __tablename__ = 'fixed_costs'
    __table_args__ = {'extend_existing': True}
    year_month = Column(String(10), primary_key=True)
    price = Column(Integer, nullable=False)
    fixed_category_id = Column(Integer, ForeignKey('fixed_costs_categories.id'), primary_key=True)
    fixed_category: FixedCostsCategories = relationship("FixedCostsCategories", back_populates="fixedCosts", lazy="joined")

class VariableCosts(Base):
    __tablename__ = 'variable_costs'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    spending_flag = Column(Boolean, nullable=False)
    variable_category_id = Column(Integer, ForeignKey('variable_costs_categories.id'), nullable=False)
    variable_category: VariableCostsCategories = relationship("VariableCostsCategories", back_populates="variableCosts", lazy="joined")


class Totals(Base):
    __tablename__ = 'totals'
    year_month = Column(String(10), primary_key=True)
    price = Column(Integer, nullable=False)

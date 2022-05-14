
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, Date
from .database import Base

from sqlalchemy.ext.declarative import AbstractConcreteBase


class Category(AbstractConcreteBase, Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    en_name = Column(String(50), nullable=False)

class FixedCostCategory(Category):
    __tablename__ = 'fixed_cost_categories'
    __table_args__ = {'extend_existing': True}
    fixed_cost = relationship("FixedCost", back_populates="fixedCost", lazy="joined")

class VariableCostCategory(Category):
    __tablename__ = 'variable_cost_categories'
    __table_args__ = {'extend_existing': True}
    variable_cost = relationship("VariableCost", back_populates="variableCost", lazy="joined")


class FixedCost(Base):
    __tablename__ = 'fixed_costs'
    __table_args__ = {'extend_existing': True}
    year_month = Column(String(10), primary_key=True)
    price = Column(Integer, nullable=False)
    fixed_category_id = Column(Integer, ForeignKey('fixed_cost_categories.id'), primary_key=True)
    fixed_cost_category: FixedCostCategory = relationship("FixedCostCategory", back_populates="fixedCost", lazy="joined")

class VariableCost(Base):
    __tablename__ = 'variable_costs'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    spending_flag = Column(Boolean, nullable=False)
    variable_category_id = Column(Integer, ForeignKey('variable_cost_categories.id'), nullable=False)
    variable_category: VariableCostCategory = relationship("VariableCostCategory", back_populates="variableCost", lazy="joined")


class Totals(Base):
    __tablename__ = 'totals'
    year_month = Column(String(10), primary_key=True)
    price = Column(Integer, nullable=False)

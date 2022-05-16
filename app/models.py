
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

from sqlalchemy.ext.declarative import AbstractConcreteBase


class FixedCostCategory(Base):
    __tablename__ = 'fixed_cost_categories'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    en_name = Column(String(50), nullable=False)
    fixed_costs = relationship("FixedCost", back_populates='fixed_cost_category')

class VariableCostCategory(Base):
    __tablename__ = 'variable_cost_categories'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    en_name = Column(String(50), nullable=False)
    variable_costs = relationship("VariableCost", back_populates='variable_cost_category')

class FixedCost(Base):
    __tablename__ = 'fixed_costs'
    __table_args__ = {'extend_existing': True}
    year_month = Column(String(10), primary_key=True)
    price = Column(Integer, nullable=False)
    fixed_category_id = Column(Integer, ForeignKey('fixed_cost_categories.id'), primary_key=True)
    fixed_cost_category = relationship("FixedCostCategory", back_populates="fixed_costs")


class VariableCost(Base):
    __tablename__ = 'variable_costs'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(String, nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    variable_category_id = Column(Integer, ForeignKey('variable_cost_categories.id'), nullable=False)
    variable_cost_category = relationship("VariableCostCategory", back_populates="variable_costs")


class Totals(Base):
    __tablename__ = 'totals'
    year_month = Column(String(10), primary_key=True)
    price = Column(Integer, nullable=False)

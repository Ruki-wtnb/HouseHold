
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, Date
from websockets import lazy_import
from .database import Base

from sqlalchemy.ext.declarative import AbstractConcreteBase


class Category(AbstractConcreteBase, Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    en_name = Column(String(50), nullable=False)

class FixedCostCategory(Category):
    __tablename__ = 'fixed_cost_categories'
    __table_args__ = {'extend_existing': True}
    fixed_costs = relationship("FixedCost")

class VariableCostCategory(Category):
    __tablename__ = 'variable_cost_categories'
    __table_args__ = {'extend_existing': True}
    fixed_costs = relationship("VariableCost")


class FixedCost(Base):
    __tablename__ = 'fixed_costs'
    __table_args__ = {'extend_existing': True}
    year_month = Column(String(10), primary_key=True)
    price = Column(Integer, nullable=False)
    fixed_category_id = Column(Integer, ForeignKey('fixed_cost_categories.id'), primary_key=True)
    fixed_cost_category = relationship("FixedCostCategory", back_populates="fixedCosts", lazy="joined", innerjoin=True)


class VariableCost(Base):
    __tablename__ = 'variable_costs'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    spending_flag = Column(Boolean, nullable=False)
    variable_category_id = Column(Integer, ForeignKey('variable_cost_categories.id'), nullable=False)
    variable_category = relationship("VariableCostCategory",  back_populates="variableCosts", lazy="joined", innerjoin=True)


class Totals(Base):
    __tablename__ = 'totals'
    year_month = Column(String(10), primary_key=True)
    price = Column(Integer, nullable=False)

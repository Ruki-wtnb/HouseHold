
from email.policy import default
from sqlalchemy import Column, ColumnDefault, ForeignKey, Integer, String
from sqlalchemy.types import Date
from .database import Base

from sqlalchemy.ext.declarative import AbstractConcreteBase
from enum import Enum

class Categories(AbstractConcreteBase, Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50))

class FixedCategories(Categories):
    __tablename__ = 'fixed_categories'
    __table_args__ = {'extend_existing': True}

class PaymentCategories(Categories):
    __tablename__ = 'payment_categories'
    __table_args__ = {'extend_existing': True}

class SpendingCategories(Categories):
    __tablename__ = 'spending_categories'
    __table_args__ = {'extend_existing': True}


class Account(AbstractConcreteBase, Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date)
    name = Column(String(100))
    price = Column(Integer)

class FixedCosts(Base):
    __tablename__ = 'fixed_costs'
    __table_args__ = {'extend_existing': True}
    year_month = Column(String(10), primary_key=True)
    price = Column(Integer)
    fixed_id = Column(Integer, ForeignKey('fixed_categories.id'), primary_key=True)

class Incomes(Account):
    __tablename__ = 'incomes'
    __table_args__ = {'extend_existing': True}

class Spendings(Account):
    __tablename__ = 'spendings'
    __table_args__ = {'extend_existing': True}
    spending_id = Column(Integer, ForeignKey('spending_categories.id'))
    payment_id = Column(Integer, ForeignKey('payment_categories.id'))


class Totals(Base):
    __tablename__ = 'totals'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date)
    price = Column(Integer)


class CateName(str, Enum):
    SpendingCategories = "SpendingCategories"
    PaymentCategorie = "PaymentCategorie"
    FixedCategories = "FixedCategories"

class FixedName(str, Enum):
    Rent = "家賃"
    Water = "水道代"
    Electric = "電気代"
    Gas = "ガス代"
    WiFi = "WiFi代"

class SpendingName(str, Enum):
    Food = "食費"
    EatingOut = "外食費"
    Livingware = "生活用品"
    HomeAppliances = "生活家電"
    LivingFurniture = "生活家具"

class PaymentName(str, Enum):
    QR = "QR"
    Card = "Card"
    Cash = "Cash"

class Month(str, Enum):
    Jan = "Jan"
    Feb = "Feb"
    Mar = "MAr"
    Apr = "Apr"
    May = "May"
    Jun = "Jun"
    Jul = "Jul"
    Aug = "Aug"
    Sep = "Sep"
    Oct = "Oct"
    Nov = "Nov"
    Dec = "Dec"

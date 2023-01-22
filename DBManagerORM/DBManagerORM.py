
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


class DBManagerORM():

    Base = declarative_base()

    def __init__(self, db_name :str, db_protocol : str = "postgresql", user_name : str = "postgres", user_password : str = "111", host : str = "localhost", port : str = "5432") -> None:
        self.DSN = F"{db_protocol}://{user_name}:{user_password}@{host}:{port}/{db_name}"
        self.engine = sa.create_engine(self.DSN)
        tables = ['sales', 'stocks', 'books', 'shops', 'publishers']
        self.DropTable(tables)
        self.Base.metadata.create_all(self.engine)

    def GetSession(self) -> object:
        return sessionmaker(bind=self.engine)()

    def DropTable(self, tables : list):
        for table in tables:
            self.Base.metadata.drop_all(self.engine, tables=[self.Base.metadata.tables.get(table)], checkfirst=True)


class Publisher(DBManagerORM.Base):
    __tablename__ = "publishers"
    publisher_id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(length=128))

class Shop(DBManagerORM.Base):
    __tablename__ = "shops"
    shop_id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(length=128))

class Book(DBManagerORM.Base):
    __tablename__ = "books"
    book_id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.VARCHAR(120), nullable=False)
    publisher_id = sa.Column(sa.Integer, sa.ForeignKey("publishers.publisher_id"), nullable=False)

class Stock(DBManagerORM.Base):
    __tablename__ = "stocks"
    stock_id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    book_id = sa.Column(sa.Integer, sa.ForeignKey("books.book_id"), nullable=False)
    shop_id = sa.Column(sa.Integer, sa.ForeignKey("shops.shop_id"), nullable=False)
    count = sa.Column(sa.Integer, nullable=False)
    #bs_fk = sa.ForeignKeyConstraint(['book_id', 'shop_id'], ['books.book_id', 'shops.shop_id']) # ?
    
class Sale(DBManagerORM.Base):
    __tablename__ = "sales"
    sale_id = sa.Column(sa.Integer, primary_key=True)
    price = sa.Column(sa.Float, nullable=False)
    sale_date = sa.Column(sa.DateTime, nullable=False)
    count = sa.Column(sa.Integer, nullable=False)
    stock_id = sa.Column(sa.Integer, sa.ForeignKey("stocks.stock_id"), nullable=False)

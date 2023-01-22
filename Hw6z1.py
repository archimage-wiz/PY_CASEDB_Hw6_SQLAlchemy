
import json
from pprint import pprint
import sqlalchemy as sa

import DBManagerORM.DBManagerORM as dbm


if __name__ == "__main__":
    
    dbm_obj1 = dbm.DBManagerORM("Hw6_BookStock")
    session = dbm_obj1.GetSession()
    
    with open('tests_data.json', 'r') as fd:
        data = json.load(fd)
        for dat in data:
            if dat["model"] == "publisher":
                session.add(dbm.Publisher(publisher_id=dat['pk'], name=dat['fields']['name']))
                session.commit()
            if dat["model"] == "book":
                session.add(dbm.Book(book_id=dat['pk'], title=dat['fields']['title'], publisher_id=dat['fields']['id_publisher']))
                session.commit()
            if dat["model"] == "shop":
                session.add(dbm.Shop(shop_id=dat['pk'], name=dat['fields']['name']))
                session.commit()
            if dat["model"] == "stock":
                session.add(dbm.Stock(stock_id=dat['pk'], book_id=dat['fields']['id_book'], shop_id=dat['fields']['id_shop'], count=dat['fields']['count']))
                session.commit()
            if dat["model"] == "sale":
                session.add(dbm.Sale(sale_id=dat['pk'], stock_id=dat['fields']['id_stock'], price=dat['fields']['price'], sale_date=dat['fields']['date_sale'], count=dat['fields']['count']))
                session.commit()
        
# requests task 2

autor_id = 1

st_q = session.query(dbm.Book.title, dbm.Shop.name, dbm.Sale.price, dbm.Sale.sale_date, dbm.Stock.stock_id) \
.join(dbm.Book, dbm.Stock.book_id == dbm.Book.book_id).filter(dbm.Book.publisher_id == autor_id) \
.join(dbm.Sale, dbm.Sale.stock_id == dbm.Stock.stock_id) \
.join(dbm.Shop, dbm.Shop.shop_id == dbm.Stock.shop_id)

#print(st_q)

for book, shop, price, date, _ in st_q.all():
    print(book[:30], shop[:15].center(15), str(price)[:15].center(15), date.date(), sep='\t'*2)





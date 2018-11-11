import sqlite3
import random

conn = sqlite3.connect('TEMP.db')

c = conn.cursor()

#c.execute("""CREATE TABLE items(
#            itemLocation text,
#            itemName text,
#            itemNumber text,
#            itemModel text,
#            date_created real,
#            date_sold real,
#            date_updated real,
#            weight real,
#            itemPrice real,
#            itemQty integer
#            )""")
#
#c.execute("""CREATE TABLE locations(
#             itemNumPrefix text,
#             available boolean,
#             numAvailable int
#             )""")



def initializeItemLocations():
    alpha = "ABCD"
    side = "12"
    bay = "XYZ"
    shelf = "1234"
    itemNum = ""      
    c = conn.cursor()           
    for a in alpha:
       for b in side:
           for cc in bay:
               for d in shelf:
                   itemNum = a+b+cc+d
                   with conn:
                       c.execute("INSERT INTO locations VALUES(:itemNumPrefix, :available ,:numAvailable)", {'itemNumPrefix': itemNum, 'available': True,'numAvailable': 10})
    with conn:     
        c.execute("SELECT * FROM locations")
        data = c.fetchall()
        print(data)

#initializeItemLocations()

def insertItem(name, model, quantity, wPrice, rPrice, avail):
    c.execute("SELECT itemNumPrefix FROM locations WHERE numAvailable>=:numAvailable",{'numAvailable':quantity})
    itemLocation = c.fetchone()
    c.execute("INSERT INTO items VALUES(:itemName, :itemNumber, :itemModel, :date_created, :date_sold, :date_updated, :weight, :itemPrice, :itemQty)",{'itemName': name, 'itemNumber':itemLocation[0], 'itemModel':model, 'date_created': 9.9, 'date_sold': 9.9, 'date_updated':9.9, 'weight': 9.9, 'itemPrice': rPrice, 'itemQty':quantity})
    c.execute("SELECT * FROM items")
    print(c.fetchall())
    
    


# def insertItem(name, number, created, sold, updated, weight, price):
#     with conn:
#         c.execute("INSERT INTO itms VALUES(:itemName, :itemNumber, :date_created, :date_sold, :date_updated,:weight,:price)", {'itemName':name, 'itemNumber': number,'date_created':created, 'date_sold':sold, 'date_updated':updated, 'weight':weight, 'itemPrice':price})

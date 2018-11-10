import sqlite3

conn = sqlite3.connect('TEMP.db')

c = conn.cursor()

#c.execute("""CREATE TABLE items(
#            itemLocation text,
#            itemName text,
#            itemNumber text,
#            date_created real,
#            date_sold real,
#            date_updated real,
#            weight real,
#            itemPrice real,
#            itemQty integer
#            )""")

#c.execute("""CREATE TABLE locations(
#             itemNumPrefix text,
#             available boolean,
#             numOccuppied int
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

initializeItemLocations()

def insertItem(name, quantity, wPrice, rPrice, avail = 1):
    c.execute("SELECT itemNumPrefix FROM locations WHERE available =:available ND", {'available':avail})
    for i in c.fetchall():
        if(available == True):
            print("it might be working")
            break
        else:
            continue
    c.fetchone

# def insertItem(name, number, created, sold, updated, weight, price):
#     with conn:
#         c.execute("INSERT INTO itms VALUES(:itemName, :itemNumber, :date_created, :date_sold, :date_updated,:weight,:price)", {'itemName':name, 'itemNumber': number,'date_created':created, 'date_sold':sold, 'date_updated':updated, 'weight':weight, 'itemPrice':price})

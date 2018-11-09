import sqlite3

conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute("""CREATE TABLE items(
            pID int,
            itemName text,
            itemNumber text,
            date_created date,
            date_sold date,
            date_updated date,
            weight real,
            itemPrice real
            )""")

c.execute("""CREATE TABLE items(
            location text,
            avail_status boolean
            )""")
# All possible locations and status of availablity
All_Locations = {
    "A1X1":True,
    "A1X2":True,
    "A1X3":True,
    "A1X4":True,
    "A1Y1":True,
    "A1Y2":True,
    "A1Y3":True,
    "A1Y4":True,
    "A1Z1":True,
    "A1Z2":True,
    "A1Z3":True,
    "A1Z4":True,
    "A2X1":True,
    "A2X2":True,
    "A2X3":True,
    "A2X4":True,
    "A2Y1":True,
    "A2Y2":True,
    "A2Y3":True,
    "A2Y4":True,
    "A2Z1":True,
    "A2Z2":True,
    "A2Z3":True,
    "A2Z4":True,
    "B1X1":True,
    "B1X2":True,
    "B1X3":True,
    "B1X4":True,
    "B1Y1":True,
    "B1Y2":True,
    "B1Y3":True,
    "B1Y4":True,
    "B1Z1":True,
    "B1Z2":True,
    "B1Z3":True,
    "B1Z4":True,
    "B2X1":True,
    "B2X2":True,
    "B2X3":True,
    "B2X4":True,
    "B2Y1":True,
    "B2Y2":True,
    "B2Y3":True,
    "B2Y4":True,
    "B2Z1":True,
    "B2Z2":True,
    "B2Z3":True,
    "B2Z4":True,
    "C1X1":True,
    "C1X2":True,
    "C1X3":True,
    "C1X4":True,
    "C1Y1":True,
    "C1Y2":True,
    "C1Y3":True,
    "C1Y4":True,
    "C1Z1":True,
    "C1Z2":True,
    "C1Z3":True,
    "C1Z4":True,
    "C2X1":True,
    "C2X2":True,
    "C2X3":True,
    "C2X4":True,
    "C2Y1":True,
    "C2Y2":True,
    "C2Y3":True,
    "C2Y4":True,
    "C2Z1":True,
    "C2Z2":True,
    "C2Z3":True,
    "C2Z4":True
}


def insertItem(name, number, created, sold, updated, weight, price):
    with conn:
        c.execute("INSERT INTO itms VALUES(:itemName, :itemNumber, :date_created, :date_sold, :date_updated,:weight,:price)", {'itemName':name, 'itemNumber': number,'date_created':created, 'date_sold':sold, 'date_updated':updated, 'weight':weight, 'itemPrice':price})





# alpha = "ABC"
# side = "12"
# bay = "XYZ"
# shelf = "1234"
#
#
# for a in alpha:
#     for b in side:
#         for c in bay:
#             for d in shelf:
#                 print("\""+a+b+c+d+"\":True,")

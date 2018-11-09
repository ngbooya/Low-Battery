import sqlite3

conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute("""CREATE TABLE items(
            itemLocation text,
            itemName text,
            itemNumber text,
            date_created real,
            date_sold real,
            date_updated real,
            weight real,
            itemPrice real,
            itemQty integer
            )""")

# c.execute("""CREATE TABLE items(
#             location text,
#             avail_status boolean
#             )""")


# All possible locations and status of availablity
All_Locations = {
    "A1X1":(True, 0),
    "A1X2":(True, 0),
    "A1X3":(True, 0),
    "A1X4":(True, 0),
    "A1Y1":(True, 0),
    "A1Y2":(True, 0),
    "A1Y3":(True, 0),
    "A1Y4":(True, 0),
    "A1Z1":(True, 0),
    "A1Z2":(True, 0),
    "A1Z3":(True, 0),
    "A1Z4":(True, 0),
    "A2X1":(True, 0),
    "A2X2":(True, 0),
    "A2X3":(True, 0),
    "A2X4":(True, 0),
    "A2Y1":(True, 0),
    "A2Y2":(True, 0),
    "A2Y3":(True, 0),
    "A2Y4":(True, 0),
    "A2Z1":(True, 0),
    "A2Z2":(True, 0),
    "A2Z3":(True, 0),
    "A2Z4":(True, 0),
    "B1X1":(True, 0),
    "B1X2":(True, 0),
    "B1X3":(True, 0),
    "B1X4":(True, 0),
    "B1Y1":(True, 0),
    "B1Y2":(True, 0),
    "B1Y3":(True, 0),
    "B1Y4":(True, 0),
    "B1Z1":(True, 0),
    "B1Z2":(True, 0),
    "B1Z3":(True, 0),
    "B1Z4":(True, 0),
    "B2X1":(True, 0),
    "B2X2":(True, 0),
    "B2X3":(True, 0),
    "B2X4":(True, 0),
    "B2Y1":(True, 0),
    "B2Y2":(True, 0),
    "B2Y3":(True, 0),
    "B2Y4":(True, 0),
    "B2Z1":(True, 0),
    "B2Z2":(True, 0),
    "B2Z3":(True, 0),
    "B2Z4":(True, 0),
    "C1X1":(True, 0),
    "C1X2":(True, 0),
    "C1X3":(True, 0),
    "C1X4":(True, 0),
    "C1Y1":(True, 0),
    "C1Y2":(True, 0),
    "C1Y3":(True, 0),
    "C1Y4":(True, 0),
    "C1Z1":(True, 0),
    "C1Z2":(True, 0),
    "C1Z3":(True, 0),
    "C1Z4":(True, 0),
    "C2X1":(True, 0),
    "C2X2":(True, 0),
    "C2X3":(True, 0),
    "C2X4":(True, 0),
    "C2Y1":(True, 0),
    "C2Y2":(True, 0),
    "C2Y3":(True, 0),
    "C2Y4":(True, 0),
    "C2Z1":(True, 0),
    "C2Z2":(True, 0),
    "C2Z3":(True, 0),
    "C2Z4":(True, 0)
}


# def insertItem(name, number, created, sold, updated, weight, price):
#     with conn:
#         c.execute("INSERT INTO itms VALUES(:itemName, :itemNumber, :date_created, :date_sold, :date_updated,:weight,:price)", {'itemName':name, 'itemNumber': number,'date_created':created, 'date_sold':sold, 'date_updated':updated, 'weight':weight, 'itemPrice':price})





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
#                 print("\""+a+b+c+d+"\":(True, 0),")

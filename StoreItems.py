import sqlite3
import random
import csv
import tkinter as tk
from Database_Test import initializeTABLES
import datetime

conn = sqlite3.connect('MotherLoad.db')

c = conn.cursor()


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

# def initializeSoftware():
#     c = conn.cursor()
#
#     c.execute("""CREATE TABLE employees(
#                 first text,
#                 last text,
#                 username text,
#                 password text,
#                 email text
#                 )""")
#
#     c.execute("""CREATE TABLE items(
#                itemName text,
#                itemNumber text,
#                itemModel text,
#                date_created text,
#                date_sold text,
#                date_updated text,
#                weight real,
#                itemPrice real,
#                itemQty integer
#                )""")
#
#     c.execute("""CREATE TABLE locations(
#                 itemNumPrefix text,
#                 available boolean,
#                 numAvailable int
#                 )""")
#
#     alpha = "ABCD"
#     side = "12"
#     bay = "XYZ"
#     shelf = "1234"
#     itemNum = ""
#     c = conn.cursor()
#     for a in alpha:
#        for b in side:
#            for cc in bay:
#                for d in shelf:
#                    itemNum = a+b+cc+d
#                    with conn:
#                        c.execute("INSERT INTO locations VALUES(:itemNumPrefix, :available ,:numAvailable)", {'itemNumPrefix': itemNum, 'available': True,'numAvailable': 10})
#     with conn:
#         c.execute("SELECT * FROM locations")
#         data = c.fetchall()
#         print(data)        # Attempt of Initialize Software Function

# initializeItemLocations()

def insertItem(name, model, upc, quantity, wPrice, rPrice):
    conn = sqlite3.connect('MotherLoad.db')
    c = conn.cursor()
    c.execute("SELECT itemNumPrefix FROM locations WHERE numAvailable>=:numAvailable",{'numAvailable':quantity})
    itemLocationList = c.fetchone()
    itemLocation = itemLocationList[0]
    c.execute("SELECT numAvailable FROM locations WHERE itemNumPrefix=:itemNumPrefix",{'itemNumPrefix':itemLocation})
    availabilityAtLocation = c.fetchone()[0]
    current_date = datetime.datetime.now().strftime("%m-%d-%y")
    retailVal = int(quantity) * float(rPrice)
    wholesaleVal = int(quantity) * float(wPrice)
    with conn:
        c.execute("INSERT INTO items VALUES(:itemName, :itemNumber, :itemModel, :UPC, :date_created, :wholesalePrice, :itemPrice, :wWorth, :rWorth, :itemQty)",{'itemName': name, 'itemNumber':itemLocation, 'itemModel':model, 'UPC':upc, 'date_created': current_date, 'wholesalePrice': wPrice, 'itemPrice': rPrice, 'itemQty':quantity, 'wWorth':wholesaleVal, 'rWorth':retailVal})
        conn.commit()
    conn.close()

#    c.execute("SELECT * FROM items")
    # print(c.fetchall())
    conn = sqlite3.connect('MotherLoad.db')
    c = conn.cursor()
    updatedAvailability = int(availabilityAtLocation) - int(quantity)
    updateAvailability(itemLocation, updatedAvailability)
    conn.close()

def updateAvailability(itemLoc, updatedAvail):
    with conn:
            c.execute("""UPDATE locations SET numAvailable=:numAvailable WHERE itemNumPrefix=:itemNumPrefix""",{'numAvailable':updatedAvail, 'itemNumPrefix':itemLoc})
            conn.commit()



def exportCSV():
    with conn:
        csvWriter = csv.writer(open("output.csv", "w"))
        c.execute("SELECT * FROM items")
        rows = c.fetchall()
        csvWriter.writerows(rows)

def searchItem(iName,iUPC):
    if iName != "":
        c.execute("SELECT * FROM items WHERE itemName=:itemName", {'itemName': iName})
        searchResult = c.fetchall()
        numOfResults = len(searchResult)
        outputString = ""
        for i in range(numOfResults):
            for j in searchResult[i]:
                outputString = outputString + str(j) + " | "
            outputString = outputString + "\n"

        searchResultsWindow = tk.Tk()
        searchResultsWindow.title('Results')
        searchResultsLabel = tk.Label(searchResultsWindow, text=outputString)
        searchResultsLabel.pack()

    else:
        c.execute("SELECT * FROM items WHERE UPC=:UPC", {'UPC': iUPC})
        searchResult = c.fetchall()
        numOfResults = len(searchResult)
        outputString = ""
        for i in range(numOfResults):
            for j in searchResult[i]:
                outputString = outputString + str(j) + " | "
            outputString = outputString + "\n"

        searchResultsWindow = tk.Tk()
        searchResultsWindow.title('Results')
        searchResultsLabel = tk.Label(searchResultsWindow, text=outputString)
        searchResultsLabel.pack()



def lowInventory():
    c.execute("SELECT * FROM items WHERE itemQty<=:itemQty", {'itemQty':2})
    results = c.fetchall()
    lowStockWindow = tk.Tk()
    lowStockWindow.title('Low Stock Items')
    lowStockLabel = tk.Label(lowStockWindow, text=results)
    lowStockLabel.pack()

def profitPotential():
    c.execute("SELECT SUM(wWorth) FROM items")
    wVal = c.fetchone()[0]
    c.execute("SELECT SUM(rWorth) FROM items")
    rVal = c.fetchone()[0]
    potentialProfit = round(rVal,2) - round(wVal,2)
    print(round(potentialProfit,2))
    ppWindow = tk.Tk()
    printOut = "Your warehouse inventory is worth: $" + str(round(wVal,2)) + "\n" + "Retail value is: $" + str(round(rVal,2)) + "\n" + "\nProfit Potential is: $" + str(round(potentialProfit,2))
    ppMessage = tk.Message(ppWindow, text=printOut, width=400)
    ppMessage.pack()



def removeItems(iName):
    with conn:
        c.execute("DELETE FROM items WHERE itemName=:itemName", {'itemName':iName})

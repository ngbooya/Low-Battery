import sqlite3
import random
import csv
import tkinter as tk

conn = sqlite3.connect('TEMP.db')

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

# initializeItemLocations()

def insertItem(name, model, quantity, wPrice, rPrice, avail):
    c.execute("SELECT itemNumPrefix FROM locations WHERE numAvailable>=:numAvailable",{'numAvailable':quantity})
    itemLocation = c.fetchone()

    with conn:
        c.execute("INSERT INTO items VALUES(:itemName, :itemNumber, :itemModel, :date_created, :date_sold, :date_updated, :weight, :itemPrice, :itemQty)",{'itemName': name, 'itemNumber':itemLocation[0], 'itemModel':model, 'date_created': "10-18-2018", 'date_sold': "11-16-2018", 'date_updated':"10-18-2018", 'weight': 1.12, 'itemPrice': rPrice, 'itemQty':quantity})

    c.execute("SELECT * FROM items")
    # print(c.fetchall())

def exportCSV():
    with conn:
        csvWriter = csv.writer(open("output.csv", "w"))
        c.execute("SELECT * FROM items")
        rows = c.fetchall()

        csvWriter.writerows(rows)

def searchItem(iName):
    c.execute("SELECT * FROM items WHERE itemName=:itemName", {'itemName': iName})
    searchResult = c.fetchall()

    searchResultsWindow = tk.Tk()
    searchResultsWindow.title('Results')
    searchResultsLabel = tk.Label(searchResultsWindow, text=searchResult)
    searchResultsLabel.pack()

def lowInventory():
    c.execute("SELECT * FROM items WHERE itemQty<=:itemQty", {'itemQty':2})
    results = c.fetchall()
    lowStockWindow = tk.Tk()
    lowStockWindow.title('Low Stock Items')
    lowStockLabel = tk.Label(lowStockWindow, text=results)
    lowStockLabel.pack()

def salesAnalysis():
    c.execute("SELECT *, SUM(itemPrice) FROM items GROUP BY itemName ORDER BY SUM(itemPrice) DESC")
    print(c.fetchall())

def removeItems(iName):
    with conn:
        c.execute("DELETE FROM items WHERE itemName=:itemName", {'itemName':iName})

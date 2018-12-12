import sqlite3
import csv
import tkinter as tk

class Employee:

    #Constructor
    def __init__(self,first, last, username, password, email, manager):
        self.first = first
        self.last = last
        self.username = username
        self.password = password
        self.email = email
        self.manager = manager
    def email(self):
        return '{} {}@email.com'.format(self.first, self.last)

    def fullname(self):
        return '{} {}'.format(self.first, self.last)
    def __repr__(self):
        return "Employee('{}','{}','{}')".format(self.first, self.last,self.username, self.password, self.email)

class Item:

    #Constructor
    def __init__(self,itemName, itemNumber, quantity, wPrice, rPRice):
        self.itemName = itemName
        self.itemNumber = itemNumber
        self.quantity = quantity
        self.wPrice = wPrice
        self.rPrice= rPrice



#Open connection
conn = sqlite3.connect('MotherLoad.db')
# #
# # # Use cursor to run SQL commands
c = conn.cursor()
def initializeTABLES():
    c.execute("""CREATE TABLE employees(
                first text,
                last text,
                username text,
                password text,
                email text,
                manager text
                )""")

    c.execute("""CREATE TABLE timesheet(
            username text,
            work_date datetime,
            clockInTime text,
            clockOutTime text
            )""")

    c.execute("""CREATE TABLE items(
               itemName text,
               itemNumber text,
               itemModel text,
               UPC text,
               date_created datetime,
               wholesalePrice real,
               itemPrice real,
               wWorth real,
               rWorth real,
               itemQty integer
               )""")

    c.execute("""CREATE TABLE locations(
                itemNumPrefix text,
                available boolean,
                numAvailable int
                )""")
# initializeTABLES()
#


def insert_emp(emp):
    with conn:
        c.execute("SELECT username FROM employees WHERE username==:username",{'username':emp.username})
    existingUser = c.fetchone()
    if existingUser == None:
        with conn:
            c.execute("INSERT INTO employees VALUES(:first, :last ,:username,:password, :email, :manager)", {'first': emp.first, 'last': emp.last,'username':emp.username, 'password': emp.password, 'email':emp.email, 'manager':emp.manager })
        creationSuccessWindow = tk.Tk()
        creationSuccessWindow.title('New Employee')
        creationSuccessLabel = tk.Label(creationSuccessWindow, text="Account Created Successfully")
        creationSuccessLabel.pack()
    else:
        creationSuccessWindow = tk.Tk()
        creationSuccessWindow.title('New Employee')
        creationSuccessLabel = tk.Label(creationSuccessWindow, text="User exists. Please try another username")
        creationSuccessLabel.pack()

def userAuthentication(uname, pword):

    c.execute("SELECT * FROM employees WHERE username=:username and password=:password", {'username':uname, 'password':pword})
    data=c.fetchall()

    if len(data) == 0:
        return False
    else:
        return True

def get_emps_by_name(lastname):
    c.execute("SELECT * FROM employees WHERE last=:last",{'last':lastname})

    return c.fetchall()

def employeeExists(fname, lname):
    c.execute("SELECT last FROM employees WHERE last=:last and first=:first",{'first':fname, 'last':lname})

    if len(c.fetchall()) >= 1:
        return True
    else:
        return False

def remove_emp(fname, lname):
    with conn:
        c.execute("DELETE from employees WHERE first = :first and last = :last",
                    {'first':fname, 'last':lname})

def getEmailFromUsername(e):
    c.execute("SELECT email FROM employees WHERE username=:username",{'username':e})
    return c.fetchall()

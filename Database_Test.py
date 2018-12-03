import sqlite3

class Employee:

    #Constructor
    def __init__(self,first, last, username, password, email):
        self.first = first
        self.last = last
        self.username = username
        self.password = password
        self.email = email
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

#    def email(self):
#        return '{} {}@email.com'.format(self.first, self.last)
#
#    def fullname(self):
#        return '{} {}'.format(self.first, self.last)
#    def __repr__(self):
#        return "Employee('{}','{}','{}')".format(self.first, self.last,self.username, self.password, self.email)


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
                email text
                )""")

    c.execute("""CREATE TABLE timesheet(
            username text,
            date datetime,
            clockInHour int,
            clockInMinute int,
            clockOutHour int,
            clockOutMinute
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



def insert_emp(emp):
    with conn:
        c.execute("INSERT INTO employees VALUES(:first, :last ,:username,:password, :email)", {'first': emp.first, 'last': emp.last,'username':emp.username, 'password': emp.password, 'email':emp.email })

def userAuthentication(uname, pword):
    # status = c.execute("SELECT EXISTS(SELECT * FROM employees WHERE username=:username AND password=:password)", {'username':uname, 'password':pword})
    #
    # return status

    c.execute("SELECT * FROM employees WHERE username=:username and password=:password", {'username':uname, 'password':pword})
    data=c.fetchall()

    if len(data) == 0:
        return False
    else:
        return True

def get_emps_by_name(lastname):
    c.execute("SELECT * FROM employees WHERE last=:last",{'last':lastname})

    return c.fetchall()

# def update_password(emp, password):
#    with conn:
#        c.execute("""UPDATE employees SET password = :password
#                    WHERE first = :first AND last = :last""",
#                    {'first': emp.first, 'last': emp.last, 'password':password})

def remove_emp(fname, lname):
    with conn:
        c.execute("DELETE from employees WHERE first = :first and last = :last",
                    {'first':fname, 'last':lname})

def getEmailFromUsername(e):
    c.execute("SELECT email FROM employees WHERE username=:username",{'username':e})
    return c.fetchall()


#conn.close()

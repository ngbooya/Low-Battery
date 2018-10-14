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



#Open connection
conn = sqlite3.connect('TEMP.db')
# #
# # # Use cursor to run SQL commands
c = conn.cursor()
#
#c.execute("""CREATE TABLE employees(
#             first text,
#             last text,
#             username text,
#             password text,
#             email text
#             )""")

def insert_emp(emp):
    with conn:
        c.execute("INSERT INTO employees VALUES(:first, :last ,:username,:password, :email)", {'first': emp.first, 'last': emp.last,'username':emp.username, 'password': emp.password, 'email':emp.email })

# def insert_emp(emp):
#     with conn:
#         c.execute("INSERT INTO employees VALUES(:first, :last ,:password)", {'first': first, 'last': last, 'password': password })


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

#def update_password(emp, password):
#    with conn:
#        c.execute("""UPDATE employees SET password = :password
#                    WHERE first = :first AND last = :last""",
#                    {'first': emp.first, 'last': emp.last, 'password':password})



def remove_emp(emp):
    with conn:
        c.execute("DELETE from employees WHERE first = :first and last = :last",
                    {'first':emp.first, 'last':emp.last})
        
def getEmailFromUsername(e):
    c.execute("SELECT email FROM employees WHERE username=:username",{'username':e})
    return c.fetchall()


# def login():
#     while True:
#         username = input("Please enter your username")
#         password = input("Please enter your password")
#         with sqlite3.connect("Quiz.db") as db:
#             cursor = db.cursor()
#         find_user = ("SELECT *  FROM users WHERE username = ?")


# fName = input('Enter first name: ')
# lName = input('Enter last name: ')
# pWord = input('Enter password: ')

# emp1 = Employee(fName, lName, pWord)
#
# insert_emp(emp1)
#
# print(get_emps_by_name('Nguyen'))

# emp1 = Employee("Kevin", "Nguyen", "1234")
#
# #Close connection
#conn.close()

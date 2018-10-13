import sqlite3

class Employee:

    #Constructor
    def __init__(self,first, last, password):
        self.first = first
        self.last = last
        self.password = password
    def email(self):
        return '{} {}@email.com'.format(self.first, self.last)

    def fullname(self):
        return '{} {}'.format(self.first, self.last)
    def __repr__(self):
        return "Employee('{}','{}','{}')".format(self.first, self.last, self.password)



#Open connection
conn = sqlite3.connect('TEMP.db')
# #
# # # Use cursor to run SQL commands
c = conn.cursor()

# c.execute("""CREATE TABLE employees(
#             first text,
#             last text,
#             username text,
#             password text,
#             email text
#             )""")

def insert_emp(emp):
    with conn:
        c.execute("INSERT INTO employees VALUES(:first, :last ,:password)", {'first': emp.first, 'last': emp.last, 'password': emp.password })

# def insert_emp(emp):
#     with conn:
#         c.execute("INSERT INTO employees VALUES(:first, :last ,:password)", {'first': first, 'last': last, 'password': password })

def get_emps_by_name(lastname):
    c.execute("SELECT * FROM employees WHERE last=:last",{'last':lastname})
    return c.fetchall()

def update_password(emp, password):
    with conn:
        c.execute("""UPDATE employees SET password = :password
                    WHERE first = :first AND last = :last""",
                    {'first': emp.first, 'last': emp.last, 'password':password})

def remove_emp(emp):
    with conn:
        c.execute("DELETE from employees WHERE first = :first and last = :last",
                    {'first':emp.first, 'last':emp.last})

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
# conn.close()

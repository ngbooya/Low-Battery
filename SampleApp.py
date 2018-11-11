import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import *

# Import databases for query use
from Database_Test import *
from StoreItems import *
import smtplib
import random
import datetime

#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

aisle = "ABCD"
side = "12"
bay = "XYZ"
shelf = "1234"
stockNumberList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
itemNumber = ''
dictionary = {}
for w in aisle:
    for x in side:
        for y in bay:
            for z in shelf:
                for s in stockNumberList:
                    itemNumber = w + x + y + z + "-" + str(s)
                    dictionary[itemNumber]= 10 #dictionary returns number of available spaces; zero = Full

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LogIn, HomePage, AccountCreate, ForgotPass, ViewAll, TimeClock, AddItem, Search):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LogIn")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class LogIn(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        userNameLabel = tk.Label(self, text="Username", font=controller.title_font)
        userNameLabel.pack(side="top", fill="x", pady=10)
        userNameLabel = tk.Entry(self)
        userNameLabel.pack()

        userPasswordLabel = tk.Label(self, text="Password", font=controller.title_font)
        userPasswordLabel.pack(side="top", fill="x", pady=10)
        userPasswordLabel = tk.Entry(self, show="*")
        userPasswordLabel.pack()

        def verify():

            print("Status", userAuthentication(userNameLabel.get(),userPasswordLabel.get()))
            print("User",userNameLabel.get())
            print("Password",userPasswordLabel.get())

            if(userAuthentication(userNameLabel.get(),userPasswordLabel.get())):
                print("You are now logged in")
            else:
                print("Invalid username and password")

        # button1 = tk.Button(self, text="Login",
        #                     command=lambda # : controller.show_frame("HomePage"))
        def callback():
            verify()
            if(userAuthentication(userNameLabel.get(),userPasswordLabel.get())):
                controller.show_frame("HomePage")

        button1 = tk.Button(self, text="Login", command=callback)

        button2 = tk.Button(self, text="New User",
                            command=lambda: controller.show_frame("AccountCreate"))
        button3 = tk.Button(self, text="Forgot Password",
                            command=lambda: controller.show_frame("ForgotPass"))
        button1.pack(pady=2)
        button2.pack(pady=2)
        button3.pack(pady=2)


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        addItemButton = tk.Button(self, text="Add Item", font=controller.title_font,
                                  command=lambda: controller.show_frame("AddItem"))
        addItemButton.pack(padx=20, pady=10)

        searchLabel = tk.Button(self, text="Search", font=controller.title_font,
                                command = lambda: controller.show_frame("Search"))
        searchLabel.pack(padx=20, pady=10)

        lowStock = tk.Button(self, text="Low Stock Items", font=controller.title_font)
        ''', command=lambda:)'''
        lowStock.pack(padx=20, pady=10)

        viewAllButton = tk.Button(self, text="View All Employees", font=controller.title_font,
                                  command=lambda: controller.show_frame("ViewAll"))
        #viewAllLabel.pack(side="top", fill="x", pady=10)
        viewAllButton.pack(padx=20, pady=10)

        timeClock = tk.Button(self, text="Clock In/Out", font=controller.title_font,
                                  command=lambda: controller.show_frame("TimeClock"))
        timeClock.pack(padx=20, pady=10)
        newLabel = tk.Button(self, text="New/Discontinue", font=controller.title_font)
        newLabel.pack(padx=20, pady=10)

        button = tk.Button(self, text="Logout",
                           command=lambda: controller.show_frame("LogIn"))
        button.pack()


class AccountCreate(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        FirstName_Label = tk.Label(self, text="Enter first name", font=controller.title_font)
        FirstName_Label.pack(side="top", fill="x", pady=10)
        FirstName_Label = tk.Entry(self)
        FirstName_Label.pack()

        LastName_Label = tk.Label(self, text="Enter last name", font=controller.title_font)
        LastName_Label.pack(side="top", fill="x", pady=10)
        LastName_Label = tk.Entry(self)
        LastName_Label.pack()

        UserName_Label = tk.Label(self, text="Desired username", font=controller.title_font)
        UserName_Label.pack(side="top", fill="x", pady=10)
        UserName_Label = tk.Entry(self)
        UserName_Label.pack()

        Password_Label = tk.Label(self, text="Enter password", font=controller.title_font)
        Password_Label.pack(side="top", fill="x", pady=10)
        Password_Label = tk.Entry(self)
        Password_Label.pack()

        Email_Label = tk.Label(self, text="Enter email", font=controller.title_font)
        Email_Label.pack(side="top", fill="x", pady=10)
        Email_Label = tk.Entry(self)
        Email_Label.pack()

        # Saves new user information into database
        def getUserInfo():
            fName = FirstName_Label.get()
            lName = LastName_Label.get()
            uName = UserName_Label.get()
            pWord = Password_Label.get()
            eMail = Email_Label.get()

            # Need to senta
            # conn = sqlite3.connect(':memeory:')
            # c = conn.cursor()

            emp1 = Employee(fName,lName,uName, pWord, eMail)
            insert_emp(emp1)
            creationSuccessWindow = tk.Tk()
            creationSuccessLabel = tk.Label(creationSuccessWindow, text="Account Created Successfully")
            creationSuccessLabel.pack()
#            print(get_emps_by_name("miranda"))


            # conn.close()

            # self.FirstName_Label.config(text=fName)


        SubmitButton = tk.Button(self, text="Submit", command=getUserInfo)
        SubmitButton.pack()




        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("LogIn"))
        button.pack()



class ForgotPass(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        global entry

        ForgotPass_UserName = tk.Label(self, text="Enter your username", font=controller.title_font)
        ForgotPass_UserName.pack(side="top", fill="x", pady=10)
        entry = tk.Entry(self)
        entry.pack()
        def update_password(uname, pword):
            with conn:
                    c.execute("""UPDATE employees SET password = :password
                              WHERE username = :username""",{'username':uname, 'password':pword})
        def sendEmail():
            userInput = entry.get()
            print(userInput)
            print (getEmailFromUsername(userInput)[0])
            email = getEmailFromUsername(userInput)[0]
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("lowbattery362@gmail.com", "longestpasswordever")
            password = ""
            for i in range(8):
                password += str(random.randint(0,9))
            msg = "\nYour temporary password is: " + password
            server.sendmail("lowbattery362@gmail.com", email, msg)
            server.quit()
            update_password(userInput, password)

        b1 = tk.Button(self, text="Request Password",
                          command=sendEmail)
        b1.pack()

        b2 = tk.Button(self, text="Go Back",
                          command=lambda: controller.show_frame("LogIn"))
        b2.pack()

class ViewAll(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


        def viewAllEmployees():
            i = 1
            allEmployees = ""
            with conn:
                    c.execute("SELECT * FROM employees")
                    data = c.fetchall()
                    textEmployeeFile = open("employeeInfo.txt",'w')
                    textEmployeeFile.close()
                    for row in data:
#                        allEmployees = "\nEmployee:" + str(i)
                        textEmployeeFile = open("employeeInfo.txt",'a')
                        textEmployeeFile.write("\nEmployee:" + str(i) + "\n")
#                        print(allEmployees)
                        for j in row:
#                            allEmployees = "\t" + str(j)
                                textEmployeeFile.write("\t" + str(j) + "\n")
#                            print(allEmployees)
                        i += 1
                    textEmployeeFile.close()
                    controller.show_frame("HomePage")

                    employeesWindow = tk.Tk()
                    employeesWindowText = tk.Text(employeesWindow)
                    fileContents = open("employeeInfo.txt", 'r')
                    textFromFile = fileContents.readlines()
                    print (textFromFile)
                    employeesWindowText.insert(INSERT, textFromFile)
                    employeesWindowText.pack(fill="none", expand=TRUE)




        button = tk.Button(self, text="View",
                           command=viewAllEmployees)
        button.place(relx=.5, rely=.5, anchor=CENTER)

class TimeClock(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        def timeStamp():
            now = datetime.datetime.now()
            datetime.time(now.hour, now.minute, now.second)
            timeStamp = "Your timestamp is: " + now.strftime("%H:%M:%S")
            timeStampWindow = tk.Tk()
            timeStampLabel = tk.Label(timeStampWindow, text=timeStamp)
            timeStampLabel.pack()
#            print("Your timestamp is: ", now.strftime("%H:%M:%S"))
            controller.show_frame("HomePage")

        timeIn = tk.Button(self, text="Clock In", font=controller.title_font,
                           command=timeStamp)
        timeIn.pack()

        timeOut = tk.Button(self, text="Clock Out", font=controller.title_font,
                           command=timeStamp)
        timeOut.pack()

class AddItem(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


        itemNameLabel = tk.Label(self, text="Item Name", font=controller.title_font)
        itemNameLabel.pack(side="top", fill="x", pady=10)
        itemNameLabel = tk.Entry(self)
        itemNameLabel.pack()
        
        itemModelLabel = tk.Label(self, text="Item Model", font=controller.title_font)
        itemModelLabel.pack(side="top", fill="x", pady=10)
        itemModelLabel = tk.Entry(self)
        itemModelLabel.pack()


        howManyLabel = tk.Label(self, text="# to add to\ninventory", font=controller.title_font)
        howManyLabel.pack(side="top", fill="x", pady=10)
        howManyLabel = tk.Entry(self)
        howManyLabel.pack()

        wholesalePriceLabel = tk.Label(self, text="Wholesale Price", font=controller.title_font)
        wholesalePriceLabel.pack(side="top", fill="x", pady=10)
        wholesalePriceLabel = tk.Entry(self)
        wholesalePriceLabel.pack()
    
        retailPriceLabel = tk.Label(self, text="Retail Price", font=controller.title_font)
        retailPriceLabel.pack(side="top", fill="x", pady=10)
        retailPriceLabel = tk.Entry(self)
        retailPriceLabel.pack()

#        for i in dictionary:
#            print(i)
#            if(int(dictionary[i]) >= int(howManyLabel.get()):
#                dictionary[i]= int(dictionary[i]) - int(howManyLabel.get())
#            else:
#                continue


        def callback():
            addConfirmationWindow = tk.Tk()
            addConfirmationLabel = tk.Label(addConfirmationWindow, text=(itemNameLabel.get()+" added to inventory successfully."))
            addConfirmationLabel.pack(side="top", fill="x", pady=10)
            insertItem(itemNameLabel.get(), itemModelLabel.get(), howManyLabel.get(), wholesalePriceLabel.get(), retailPriceLabel.get(), 1)


        button1 = tk.Button(self, text="Add New Item", command=callback)

        button2 = tk.Button(self, text="Go Back",
                            command=lambda: controller.show_frame("HomePage"))
#        button3 = tk.Button(self, text="Forgot Password",
#                            command=lambda: controller.show_frame("ForgotPass"))
        button1.pack(pady=2)
        button2.pack(pady=2)
#        button3.pack(pady=2)

class Search(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        itemNameLabel = tk.Label(self, text="Item Name", font=controller.title_font)
        itemNameLabel.pack(side="top", fill="x", pady=10)
        itemNameLabel = tk.Entry(self)
        itemNameLabel.pack()

class LowStock(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

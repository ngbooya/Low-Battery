import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import *
import webbrowser

# Import databases for query use
from Database_Test import *
from StoreItems import *
import smtplib
import random
import datetime

def launchHelp():
    webbrowser.open("https://drive.google.com/open?id=1qbiw4POe3WmgU13DojmZ2ZUwfVk1GCcW")

def install():
    initializeTABLES()
    initializeItemLocations()

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

        self.CURRENT_USER = None
        print("CURRENT USER STATUS", self.CURRENT_USER)

        self.frames = {}
        for F in (LogIn, HomePage, AccountCreate, ForgotPass, ChangePassword, ViewAll, TimeClock, AddItem, Delete ,InventoryAudit, Search, Separation, Email):
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
        controller.title('Low Battery')
        def enter(event=None):
            callback()
        userNameLabel = tk.Label(self, text="Username", font=controller.title_font)
        userNameLabel.pack(side="top", fill="x", pady=10)
        # userNameLabel.grid(row=0, column=0, pady=10)
        userNameLabel = tk.Entry(self)
        userNameLabel.pack()
        # userNameLabel.grid(row=0, column=1, pady=10)

        userPasswordLabel = tk.Label(self, text="Password", font=controller.title_font)
        userPasswordLabel.pack(side="top", fill="x", pady=10)
        # userPasswordLabel.grid(row=1, column=0, pady=10, sticky='e')
        userPasswordLabel = tk.Entry(self, show="*")
        userPasswordLabel.bind('<Return>',enter)
        userPasswordLabel.pack()
        # userPasswordLabel.grid(row=1, column=1, pady=10)


        wrongPasswordLabel = tk.Label(self, text="Incorrect username and/or password.")

        def verify():
            # print("Status", userAuthentication(userNameLabel.get(),userPasswordLabel.get()))
            controller.show_frame("LogIn")
            print("User",userNameLabel.get())
            print("Password",userPasswordLabel.get())

            if(userAuthentication(userNameLabel.get(),userPasswordLabel.get())):
                print("You are now logged in")
            else:
                print("Invalid username and password")
                wrongPasswordLabel.pack()


        # button1 = tk.Button(self, text="Login",
        #                     command=lambda # : controller.show_frame("HomePage"))
        def callback():
            verify()
            if(userAuthentication(userNameLabel.get(),userPasswordLabel.get())):
                controller.CURRENT_USER = userNameLabel.get()
                print("CURRENT USER STATUS", controller.CURRENT_USER)
                controller.show_frame("HomePage")
            userNameLabel.delete(0,END)
            userPasswordLabel.delete(0,END)

        button1 = tk.Button(self, text="Login", command=enter)

        button2 = tk.Button(self, text="New User",
                            command=lambda: controller.show_frame("AccountCreate"))
        button3 = tk.Button(self, text="Forgot Password",
                            command=lambda: controller.show_frame("ForgotPass"))
        button4 = tk.Button(self, text="Change Password",
                            command=lambda: controller.show_frame("ChangePassword"))
        button1.pack(pady=2)
        # button1.grid(ipady=2, row=3, column=1)
        button2.pack(pady=2)
        # button2.grid(ipady=2, row=4, column=1)
        button3.pack(pady=2)
        # button3.grid(ipady=2, row=5, column=1)
        button4.pack(pady=2)

        installButton = tk.Button(self, text="Install Database", command=install)
        installButton.pack()

class ChangePassword(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        userNameLabel = tk.Label(self, text="User Name", font=controller.title_font)
        userNameLabel.pack()
        userNameField = tk.Entry(self)
        userNameField.pack()

        currentPassword = tk.Label(self, text="Current Password", font=controller.title_font)
        currentPassword.pack()
        currentPasswordField = tk.Entry(self)
        currentPasswordField.pack()

        newPassword = tk.Label(self, text="New Password", font=controller.title_font)
        newPassword.pack()
        newPasswordField = tk.Entry(self)
        newPasswordField.pack()
        def updatePassword():
            with conn:
                c.execute("""UPDATE employees SET password=:password WHERE username=:username""",{'password':newPasswordField.get(), 'username':userNameField.get()})
                conn.commit()

        def callback():
            updatePassword()
            controller.show_frame("LogIn")

        updatePasswordButton = tk.Button(self, text="Update Password", command=callback)
        updatePasswordButton.pack()

class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        addItemButton = tk.Button(self, text="Add Item", font=controller.title_font,
                                  command=lambda: controller.show_frame("AddItem"))
        addItemButton.pack(padx=20, pady=10, fill='x')

        searchLabel = tk.Button(self, text="Search Items", font=controller.title_font,
                                command = lambda: controller.show_frame("Search"))
        searchLabel.pack(padx=20, pady=10, fill='x')

        deleteLabel = tk.Button(self, text="Remove Item", font=controller.title_font, command = lambda: controller.show_frame("Delete"))
        deleteLabel.pack(padx=20, pady=10, fill='x')

        lowStock = tk.Button(self, text="Low Stock Items", font=controller.title_font, command=lowInventory)
        lowStock.pack(padx=20, pady=10, fill='x')

        auditButton = tk.Button(self, text="Inventory Audit", font=controller.title_font,
                                  command=exportCSV)
        auditButton.pack(padx=20, pady=10, fill='x')

        viewAllButton = tk.Button(self, text="View All Employees", font=controller.title_font,
                                  command=lambda: controller.show_frame("ViewAll"))
        #viewAllLabel.pack(side="top", fill="x", pady=10)
        viewAllButton.pack(padx=20, pady=10, fill='x')

        termEmp = tk.Button(self, text="Terminate Employee", font=controller.title_font,
                          command=lambda: controller.show_frame("Separation"))
        termEmp.pack(padx=20, pady=10, fill='x')

        timeClock = tk.Button(self, text="Clock In/Out", font=controller.title_font,
                                  command=lambda: controller.show_frame("TimeClock"))
        timeClock.pack(padx=20, pady=10, fill='x')

        email = tk.Button(self, text="Employee Email", font=controller.title_font,
                          command=lambda: controller.show_frame("Email"))
        email.pack(padx=20, pady=10, fill='x')

        ProfitButton = tk.Button(self, text="Profit Potential", font=controller.title_font,
                          command=profitPotential)
        ProfitButton.pack(padx=20, pady=10, fill='x')

        def logoutCallback():
            controller.CURRENT_USER = None;
            print("CURRENT USER STATUS", controller.CURRENT_USER)
            controller.show_frame("LogIn")
        button = tk.Button(self, text="Logout",command=logoutCallback)
        button.pack()

        helpButton = tk.Button(self, text="Help",
                           command=launchHelp)
        helpButton.pack(pady=10)

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
        Password_Label = tk.Entry(self, show="*")
        Password_Label.pack()

        Email_Label = tk.Label(self, text="Enter email", font=controller.title_font)
        Email_Label.pack(side="top", fill="x", pady=10)
        Email_Label = tk.Entry(self)
        Email_Label.pack()

        managerLabel = tk.Label(self, text="Manager? (Yes/No)", font=controller.title_font)
        managerLabel.pack(side="top", fill="x", pady=10)
        managerEntry = tk.Entry(self)
        managerEntry.pack()

        # Saves new user information into database
        def getUserInfo():
            fName = FirstName_Label.get()
            lName = LastName_Label.get()
            uName = UserName_Label.get()
            pWord = Password_Label.get()
            eMail = Email_Label.get()
            manager = managerEntry.get().upper()
            emp1 = Employee(fName,lName,uName, pWord, eMail, manager)
            insert_emp(emp1)
            creationSuccessWindow = tk.Tk()
            creationSuccessLabel = tk.Label(creationSuccessWindow, text="Account Created Successfully")
            creationSuccessLabel.pack()
            FirstName_Label.delete(0,END)
            LastName_Label.delete(0,END)
            UserName_Label.delete(0,END)
            Password_Label.delete(0,END)
            Email_Label.delete(0,END)
            managerEntry.delete(0,END)

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
            entry.delete(0,END)
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
                    c.execute("SELECT first, last, username, email, manager FROM employees")
                    data = c.fetchall()
                    textEmployeeFile = open("employeeInfo.txt",'w')
                    textEmployeeFile.close()
                    for row in data:
                        textEmployeeFile = open("employeeInfo.txt",'a')
                        textEmployeeFile.write("\nEmployee:" + str(i) + "\n")
                        for j in row:
                                textEmployeeFile.write("\t" + str(j) + "\n")
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
        now = datetime.datetime.now()

        #Don't need#################################################
        def timeStamp():
            now = datetime.datetime.now()
            datetime.time(now.hour, now.minute, now.second)
            timeStamp = "Your timestamp is: " + now.strftime("%H:%M:%S")
            timeStampWindow = tk.Tk()
            timeStampLabel = tk.Label(timeStampWindow, text=timeStamp)
            timeStampLabel.pack()
            controller.show_frame("HomePage")

            date = datetime.datetime.now().strftime("%m-%d-%y")
            hour = str(now.hour)
            minute = str(now.minute)
            time = hour + ":" + minute

            print(date, time)

        def timeIn():
            currentUser = controller.CURRENT_USER
            now = datetime.datetime.now()
            datetime.time(now.hour, now.minute, now.second)
            timeStamp = now.strftime("%H:%M:%S")
            date = datetime.datetime.now().strftime("%m-%d-%y")
            with conn:
                c.execute("INSERT INTO timesheet VALUES(:username, :work_date, :clockInTime, :clockOutTime)", {'username':controller.CURRENT_USER, 'work_date':date, 'clockInTime':timeStamp, 'clockOutTime':""})
                conn.commit()
            csvWriter = csv.writer(open("timesheet.csv", "w"))
            c.execute("SELECT * FROM timesheet")
            rows = c.fetchall()
            csvWriter.writerows(rows)
            controller.show_frame("HomePage")
            timeIn = ""

        def timeOut():
            currentUser = controller.CURRENT_USER
            now = datetime.datetime.now()
            datetime.time(now.hour, now.minute, now.second)
            timeStamp = now.strftime("%H:%M:%S")
            dateOut = datetime.datetime.now().strftime("%m-%d-%y")

            with conn:
                c.execute("UPDATE timesheet SET clockOutTime=:clockOutTime WHERE username=:username AND work_date=:work_date", {'clockOutTime':timeStamp, 'username':controller.CURRENT_USER, 'work_date':dateOut})
                conn.commit()
            csvWriter = csv.writer(open("timesheet.csv", "w"))
            c.execute("SELECT * FROM timesheet")
            rows = c.fetchall()
            csvWriter.writerows(rows)
            controller.show_frame("HomePage")


        timeIn = tk.Button(self, text="Clock In", bg='green', font=controller.title_font,
                           command=timeIn)
        timeIn.pack(expand=TRUE, fill=BOTH)

        timeOut = tk.Button(self, text="Clock Out", bg='red', font=controller.title_font,
                           command=timeOut)
        timeOut.pack(expand=TRUE, fill =BOTH)

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

        UPCLabel = tk.Label(self, text="UPC", font=controller.title_font)
        UPCLabel.pack(side="top", fill="x", pady=10)
        UPCLabel = tk.Entry(self)
        UPCLabel.pack()

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

        def callback():
            addConfirmationWindow = tk.Tk()
            addConfirmationLabel = tk.Label(addConfirmationWindow, text=(itemNameLabel.get()+" added to inventory successfully."))
            addConfirmationLabel.pack(side="top", fill="x", pady=10)
            # insertItem(itemNameLabel.get().upper(), itemModelLabel.get().upper(), UPCLabel.get(), random.randint(1,10), wholesalePriceLabel.get(), retailPriceLabel.get())
            insertItem(itemNameLabel.get().upper(), itemModelLabel.get().upper(), UPCLabel.get(), int(howManyLabel.get()), wholesalePriceLabel.get(), retailPriceLabel.get())
            itemNameLabel.delete(0,END)
            itemModelLabel.delete(0,END)
            howManyLabel.delete(0,END)
            wholesalePriceLabel.delete(0,END)
            retailPriceLabel.delete(0,END)
            UPCLabel.delete(0,END)

        button1 = tk.Button(self, text="Add New Item", command=callback)

        button2 = tk.Button(self, text="Go Back",
                            command=lambda: controller.show_frame("HomePage"))
#        button3 = tk.Button(self, text="Forgot Password",
#                            command=lambda: controller.show_frame("ForgotPass"))
        button1.pack(pady=2)
        button2.pack(pady=2)

class InventoryAudit(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        exportSuccess = tk.Label(self, text="CSV Created Successfully")
        exportSuccess.pack()

class Search(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        def enter(event=None):
            callback()
        itemNameLabel = tk.Label(self, text="Item Name", font=controller.title_font)
        itemNameLabel.pack(side="top", fill="x", pady=10)
        itemNameLabel = tk.Entry(self)
        itemNameLabel.pack()

        UPCLabel = tk.Label(self, text="UPC", font=controller.title_font)
        UPCLabel.pack(side="top", fill="x", pady=10)
        UPCLabel = tk.Entry(self)
        UPCLabel.bind('<Return>',enter)
        UPCLabel.pack()

        def callback():
            searchItem(itemNameLabel.get().upper(), UPCLabel.get())
            itemNameLabel.delete(0,END)
            UPCLabel.delete(0,END)

        searchButton = tk.Button(self, text="Search", command=callback)
        searchButton.pack(pady=2)

        button = tk.Button(self, text="Go Back",
                           command=lambda: controller.show_frame("HomePage"))
        button.pack()

class LowStock(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

class Delete(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        itemNameLabel = tk.Label(self, text="Item Name", font=controller.title_font)
        itemNameLabel.pack(side="top", fill="x", pady=10)
        itemNameLabel = tk.Entry(self)
        itemNameLabel.pack()

        def callback():
            removeItems(itemNameLabel.get().upper())
            # deleteSuccess = tk.Label(self, text="Item Deleted Successfully")
            # deleteSuccess.pack()
            itemNameLabel.delete(0, END)
            successWindow = tk.Tk()
            successLabel = tk.Label(successWindow, text="Item deleted successfully")
            successLabel.pack()
        deleteButton = tk.Button(self, text="Remove Item", command=callback)
        deleteButton.pack()
        goBackButton = tk.Button(self, text="Go Back", command=lambda: controller.show_frame("HomePage"))
        goBackButton.pack()

class Separation(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        fnameLabel = tk.Label(self, text="First Name", font=controller.title_font)
        fnameLabel.pack()
        fnameEntry = tk.Entry(self)
        fnameEntry.pack()

        lnameLabel = tk.Label(self, text="Last Name", font=controller.title_font)
        lnameLabel.pack()
        lnameEntry = tk.Entry(self)
        lnameEntry.pack()

        def callback():
            user = controller.CURRENT_USER
            with conn:
                c.execute("""SELECT manager FROM employees WHERE username== :username""", {'username':user})
            managerStatus = c.fetchone()
            print(managerStatus)
            if managerStatus[0] == "YES":
                # print(employeeExists(fnameEntry.get(), lnameEntry.get()))
                if employeeExists(fnameEntry.get(), lnameEntry.get()) == True:
                    remove_emp(fnameEntry.get(), lnameEntry.get())
                    termWindow = tk.Tk()
                    name = "\n" + fnameEntry.get() + " " + lnameEntry.get() + "\nTermination complete."
                    termCompleteLabel = tk.Label(termWindow, text=name)
                    termCompleteLabel.pack()
                    # successLabel = tk.Label(self, text=name, font=controller.title_font)
                    # successLabel.pack()
                    fnameEntry.delete(0,END)
                    lnameEntry.delete(0,END)
                else:
                    termWindow = tk.Tk()
                    termCompleteLabel = tk.Label(termWindow, text="No employee by that name")
                    termCompleteLabel.pack()
            else:
                termWindow = tk.Tk()
                termCompleteLabel = tk.Label(termWindow, text="You are not a manager.")
                termCompleteLabel.pack()
            fnameLabel.delete(0,END)

        termButton = tk.Button(self, text="Terminate Employee", command=callback)
        termButton.pack()

        defaultButton = tk.Button(self, text="Go Back", command=lambda: controller.show_frame("HomePage"))
        defaultButton.pack()

class Email(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        fnameLabel = tk.Label(self, text="First Name", font=controller.title_font)
        fnameLabel.pack()
        fnameEntry = tk.Entry(self)
        fnameEntry.pack()

        lnameLabel = tk.Label(self, text="Last Name", font=controller.title_font)
        lnameLabel.pack()
        lnameEntry = tk.Entry(self)
        lnameEntry.pack()

        messageLabel = tk.Label(self, text="Enter your message below", font=controller.title_font)
        messageLabel.pack()
        messageEntry = tk.Entry(self)
        messageEntry.pack()

        def viewSingleEmail():
            with conn:
                c.execute("""SELECT email FROM employees WHERE first=:first AND last=:last""", {'first':fnameEntry.get(), 'last':lnameEntry.get()})
                emailAddress = c.fetchone()
            if(emailAddress == None):
                employeesWindow = tk.Tk()
                employeesWindowText = tk.Text(employeesWindow)
                employeesWindowText.insert(INSERT, "No email address found for: " + fnameEntry.get() + " "+ lnameEntry.get())
                employeesWindowText.pack(fill="none", expand=TRUE)
                successLabel = tk.Label(self, text="", font=controller.title_font)
                successLabel.pack()
                fnameEntry.delete(0,END)
                lnameEntry.delete(0,END)
            else:
                employeesWindow = tk.Tk()
                employeesWindowText = tk.Text(employeesWindow)
                employeesWindowText.insert(INSERT, emailAddress)
                employeesWindowText.pack(fill="none", expand=TRUE)
                successLabel = tk.Label(self, text="", font=controller.title_font)
                successLabel.pack()
                fnameEntry.delete(0,END)
                lnameEntry.delete(0,END)

        def sendEmail(list):
            if(messageEntry.get()==""):
                errorWindow = tk.Tk()
                errorWindowLabel = tk.Text(errorWindow)
                errorWindowLabel.insert(INSERT, "No message entered. Fill in message field.")
                errorWindowLabel.pack()
                print("No message entered. Fill in message field.")
                return None
            else:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login("lowbattery362@gmail.com", "longestpasswordever")
                server.sendmail("lowbattery362@gmail.com", list, messageEntry.get())
                server.quit()
                print(list)

        def viewAllEmails():
            k = 1
            with conn:
                c.execute("""SELECT email FROM employees""")
            emailAddress = c.fetchall()
            masterListString = ""
            mailingList = ""
            for i in emailAddress:
                masterListString = masterListString + str(k) + '. ' + i[0] + '\n'
                # mailingList = mailingList + i[0] + ","
                k = k + 1
            employeesWindow = tk.Tk()
            employeesWindowText = tk.Text(employeesWindow, wrap=WORD)
            employeesWindowText.insert(INSERT, masterListString)
            employeesWindowText.pack(fill="none", expand=TRUE, wrap=WORD)
            sendEmail(emailAddress)
            messageEntry.delete(0,END)




        searchButton = tk.Button(self, text="Search Single Employee", command=viewSingleEmail)
        searchButton.pack()

        searchAllButton = tk.Button(self, text="Email ALL Employees", command=viewAllEmails)
        searchAllButton.pack()

        defaultButton = tk.Button(self, text="Go Back", command=lambda: controller.show_frame("HomePage"))
        defaultButton.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

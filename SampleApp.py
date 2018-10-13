import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import *
from Database_Test import *


#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

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
        for F in (LogIn, HomePage, AccountCreate, ForgotPass):
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
        userLabel = tk.Label(self, text="Username", font=controller.title_font)
        userLabel.pack(side="top", fill="x", pady=10)
        userLabel = tk.Entry(self)
        userLabel.pack()

        userLabel = tk.Label(self, text="Password", font=controller.title_font)
        userLabel.pack(side="top", fill="x", pady=10)
        userLabel = tk.Entry(self, show="*")
        userLabel.pack()


        button1 = tk.Button(self, text="Login",
                            command=lambda: controller.show_frame("HomePage"))
        button2 = tk.Button(self, text="New User",
                            command=lambda: controller.show_frame("AccountCreate"))
        button3 = tk.Button(self, text="Forgot Password",
                            command=lambda: controller.show_frame("ForgotPass"))
        button1.pack()
        button2.pack()
        button3.pack()


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        searchLabel = tk.Button(self, text="Search", font=controller.title_font)
        searchLabel.pack()
        # searchLabel = tk.Entry(self)
        # searchLabel.pack(side="top", fill="x", pady=10)

        viewAllLabel = tk.Button(self, text="View All", font=controller.title_font)
        #viewAllLabel.pack(side="top", fill="x", pady=10)
        viewAllLabel.pack()
        newLabel = tk.Button(self, text="New/Discontinue", font=controller.title_font)
        newLabel.pack()

        button = tk.Button(self, text="LOGOUT",
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

            emp1 = Employee(fName,lName, pWord)
            insert_emp(emp1)
            print(get_emps_by_name("Nomura"))


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
        ForgotPass_UserName = tk.Label(self, text="Enter your username", font=controller.title_font)
        ForgotPass_UserName.pack(side="top", fill="x", pady=10)
        ForgotPass_UserName = tk.Entry(self)
        ForgotPass_UserName.pack()


        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("LogIn"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

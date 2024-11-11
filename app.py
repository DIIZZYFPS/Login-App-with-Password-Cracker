import tkinter as tk
from tkinter import messagebox
from db import UserDatabase
from crack import Crack

current_user = None
curr_password = None

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Simple Login App')
        self.geometry('300x200')
        self.resizable(False, False)

        self.db = UserDatabase()
        self.crack = Crack()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginScreen, CreateScreen, SecondScreen):
            page_name = F.__name__
            frame = F(parent=self, controller=self, db=self.db, crack=self.crack)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginScreen")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name == "SecondScreen":
            frame.update_label()  
        frame.tkraise()
    
    def on_close(self):
        self.db.close()
        self.destroy()


class LoginScreen(tk.Frame):
    def __init__(self, parent, controller, db, crack):
        super().__init__(parent)
        self.controller = controller
        self.db = db
        self.crack = crack

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.inner_frame = tk.Frame(self)
        self.inner_frame.grid(row=0, column=0, sticky="nsew")

        self.username_label = tk.Label(self.inner_frame, text='Username:')
        self.username_label.pack(anchor='center', pady=5)

        self.username_entry = tk.Entry(self.inner_frame)
        self.username_entry.pack(anchor='center', pady=5)

        self.password_label = tk.Label(self.inner_frame, text='Password:')
        self.password_label.pack(anchor='center', pady=5)

        self.password_entry = tk.Entry(self.inner_frame, show='*')
        self.password_entry.pack(anchor='center', pady=5)

        self.login_button = tk.Button(self.inner_frame, text='Login', command=self.login)
        self.login_button.pack(anchor='center', pady=5)

        self.create_button = tk.Button(self.inner_frame, text='Create Account', command=lambda: controller.show_frame("CreateScreen"))
        self.create_button.pack(anchor='center', pady=5)

    def login(self):
        global current_user
        global curr_password
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.db.validate_user(username, password):
            print('Login successful')
            current_user = username
            curr_password = password
            self.controller.show_frame("SecondScreen")
        else:
            print('Login failed')
            messagebox.showerror("Error", "Invalid username or password")


class CreateScreen(tk.Frame):
    def __init__(self, parent, controller, db, crack):
        super().__init__(parent)
        self.controller = controller
        self.db = db
        self.crack = crack

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.inner_frame = tk.Frame(self)
        self.inner_frame.grid(row=0, column=0, sticky="nsew")

        self.username_label = tk.Label(self.inner_frame, text='Username:')
        self.username_label.pack(anchor='center', pady=5)

        self.username_entry = tk.Entry(self.inner_frame)
        self.username_entry.pack(anchor='center', pady=5)

        self.password_label = tk.Label(self.inner_frame, text='Password:')
        self.password_label.pack(anchor='center', pady=5)

        self.password_entry = tk.Entry(self.inner_frame, show='*')
        self.password_entry.pack(anchor='center', pady=5)

        self.create_button = tk.Button(self.inner_frame, text='Create', command=self.create)
        self.create_button.pack(anchor='center', pady=5)

        self.back_button = tk.Button(self.inner_frame, text='Go Back', command=lambda: controller.show_frame("LoginScreen"))
        self.back_button.pack(anchor='center', pady=5)

    def create(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.db.add_user(username, password):
            print('Account created successfully')
            self.controller.show_frame("LoginScreen")
        else:
            print('Account creation failed')
            messagebox.showerror("Error", "Username already exists")


class SecondScreen(tk.Frame):
    def __init__(self, parent, controller, db, crack):
        super().__init__(parent)
        self.controller = controller
        self.db = db
        self.crack = crack

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.inner_frame = tk.Frame(self)
        self.inner_frame.grid(row=0, column=0, sticky="nsew")

        self.label = tk.Label(self.inner_frame, text="")
        self.label.pack(anchor='center', pady=5)

        self.crack_Label = tk.Label(self.inner_frame, text="Crack Time")
        self.crack_Label.pack(anchor='center', pady=5)

        self.crack_button = tk.Button(self.inner_frame, text="Crack Password", command=self.crack_time)
        self.crack_button.pack(anchor='center', pady=5)

        self.back_button = tk.Button(self.inner_frame, text="Go Back", command=lambda: controller.show_frame("LoginScreen"))
        self.back_button.pack(anchor='center', pady=5)

        

    def crack_time(self):
        global curr_password
        guess, elapsed_time = self.crack.brute_force(curr_password)

        if guess is None:
            print(f"Password not cracked in 30 seconds")
            response = messagebox.askquestion("Crack Time", f"Password not brute forced in 30 seconds! Run Dictionary Attack?")

            if response == 'yes':
                self.dictionary_attack()
            else:
                print("Crack Time expired")
        else:
            print(f"Password cracked: {guess} in {elapsed_time} seconds")
            response = messagebox.askquestion("Crack Time", f"Password cracked: {guess} in {elapsed_time} seconds, Run Dictionary Attack?")

            if response == 'yes':
                self.dictionary_attack()
            else:
                print("Crack Time expired")

    def dictionary_attack(self):
        global curr_password
        guess, elapsed_time = self.crack.dictionary_attack(curr_password)

        if guess is None:
            print(f"Password not cracked in 90 seconds")
            response = messagebox.askquestion("Dictionary Attack", f"Password not cracked in 90 seconds! Try again?")

            if response == 'yes':
                self.dictionary_attack()
            else:
                print("Dictionary Attack expired")
        else:
            print(f"Password cracked: {guess} in {elapsed_time} seconds")
            response = messagebox.askquestion("Dictionary Attack", f"Password cracked: {guess} in {elapsed_time} seconds, Try again?")

            if response == 'yes':
                self.dictionary_attack()
            else:
                print("Dictionary Attack expired")

    def update_label(self):
        global current_user
        self.label.config(text=f"Welcome, {current_user}")


if __name__ == '__main__':
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()

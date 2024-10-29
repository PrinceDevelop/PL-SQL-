import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font
import mysql.connector as MyConn

# Connect to MySQL Database
mydb = MyConn.connect(
    host="localhost",
    user="root",   
    password="Vinayak@wismp",   
    database="car_management"
)
print("mydb")
cursor = mydb.cursor()

user_data = {"admin": "password"}  
car_data = []  

# Function to verify user login
def login():
    username = username_entry.get()
    password = password_entry.get()

    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    
    if username in user_data and user_data[username] == password:
        messagebox.showinfo("Login Successful", f"Welcome {username}!")
        open_dashboard()
    else:
        messagebox.showerror("Error", "Invalid username or password")

# Function to register a new user
def register():
    username = username_entry.get()
    password = password_entry.get()
    
    if username in user_data:
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, password))
        mydb.commit()
        messagebox.showerror("Error", "Username already exists")
    else:
        user_data[username] = password
        messagebox.showinfo("Success", "Registration Successful! Please log in.")

# Function to open the dashboard after successful login
def open_dashboard():
    login_window.destroy()  # Close login window

    dashboard = tk.Tk()
    dashboard.config(bg="skyblue")
    dashboard.title("Car Management System - Dashboard")

    #Defining the font styles
    label_font = ("Helvetica", 8    , "bold")
    entry_font = ("Courier", 8)
    button_font = ("Verdana", 6, "bold")
    # Input fields to add new cars
    label3=tk.Label(dashboard, text="Model Name",font=label_font)
    label3.grid(row=0, column=0, padx=10, pady=10)
    model_entry = tk.Entry(dashboard,font=entry_font)
    model_entry.grid(row=0, column=1, padx=10, pady=10)

    label4=tk.Label(dashboard, text="Brand",font=label_font)
    label4.grid(row=1, column=0, padx=10, pady=10)
    brand_entry = tk.Entry(dashboard,font=entry_font)
    brand_entry.grid(row=1, column=1, padx=10, pady=10)

    label5=tk.Label(dashboard, text="Price per Day",font=label_font)
    label5.grid(row=2, column=0, padx=10, pady=10)
    price_entry = tk.Entry(dashboard,font=entry_font)
    price_entry.grid(row=2, column=1, padx=10, pady=10)

    # Car table
    columns = ("Model", "Brand", "Price_per_Day")
    car_table = ttk.Treeview(dashboard, columns=columns, show="headings")
    for col in columns:
        car_table.heading(col, text=col)
    car_table.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    # Function to add a new car to the table
    def add_car():
        model = model_entry.get()
        brand = brand_entry.get()
        price = price_entry.get()

        if model and brand and price:
            query = "INSERT INTO cars (model_name, brand, price_per_day) VALUES (%s, %s, %s)"
            cursor.execute(query, (model, brand, price))
            mydb.commit()
            load_cars()
            clear_entries()
            messagebox.showinfo("Success", "Car added successfully!")
        else:
            messagebox.showerror("Error", "Please fill all fields")

    # Function to load cars into the table
    def load_cars():
        for i in car_table.get_children():
            car_table.delete(i)  
        cursor.execute("SELECT model_name, brand, price_per_day FROM cars")
        rows = cursor.fetchall()
        for row in rows:
            car_table.insert("", tk.END, values=row)

    # Function to clear input fields
    def clear_entries():
        model_entry.delete(0, tk.END)
        brand_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)

    # Add Car Button
    button=tk.Button(dashboard, text="Add Car", command=add_car,font=button_font)
    button.grid(row=4, column=0, padx=10, pady=10)
    load_cars()

    dashboard.mainloop()

# Setup the Login/Register window
login_window = tk.Tk()
login_window.title("Car Management System - Login")

# Username and Password Input Fields
label1=tk.Label(login_window, text="Username")
label1.grid(row=0, column=0, padx=10, pady=10)
username_entry = tk.Entry(login_window)
username_entry.grid(row=0, column=1, padx=10, pady=10)

label2=tk.Label(login_window, text="Password")
label2.grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(login_window, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Login and Register Buttons
button1=tk.Button(login_window, text="Login", command=login)
button1.grid(row=2, column=0, padx=10, pady=10)
button2=tk.Button(login_window, text="Register", command=register)
button2.grid(row=2, column=1, padx=10, pady=10)

# Start the login window loop
login_window.mainloop()


import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from mysql.connector import *
from datetime import *

# Initialize customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
resultArr = []

def dbcon(code, sel):
    global resultArr
    m1 = connect(host="localhost", user="root", passwd="1999", database="bus_booking")
    c1 = m1.cursor()
    c1.execute(code)

    if sel == 1:
        resultArr = c1.fetchall()
    m1.commit()
    c1.close()
    m1.close()

def create_connection():
    """ Create a database connection. """
    connection = sqlite3.connect('bus_booking.db')
    return connection

def create_tables(cursor):
    """ Create the necessary tables. """
    cursor.executescript(''' 
    CREATE TABLE IF NOT EXISTS Bus_Routes (
        route_id INTEGER PRIMARY KEY AUTOINCREMENT,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        distance_km REAL NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Bus_Timings (
        timing_id INTEGER PRIMARY KEY AUTOINCREMENT,
        route_id INTEGER,
        departure_time TEXT NOT NULL,
        arrival_time TEXT NOT NULL,
        FOREIGN KEY (route_id) REFERENCES Bus_Routes(route_id)
    );

    CREATE TABLE IF NOT EXISTS Bus_Details (
        bus_id INTEGER PRIMARY KEY AUTOINCREMENT,
        route_id INTEGER,
        bus_type TEXT NOT NULL,
        fare REAL NOT NULL,
        seats_available INTEGER NOT NULL,
        FOREIGN KEY (route_id) REFERENCES Bus_Routes(route_id)
    );

    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone_number TEXT NOT NULL,
        password TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Bookings (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        bus_id INTEGER,
        booking_date TEXT NOT NULL,
        seat_number INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (bus_id) REFERENCES Bus_Details(bus_id)
    );
    ''')
    connection.commit()

def insert_default_data(cursor):
    """ Insert default routes, timings, and bus details if they do not already exist. """
    cursor.execute("SELECT COUNT(*) FROM Bus_Routes")
    if cursor.fetchone()[0] == 0:
        cursor.executescript(''' 
        INSERT INTO Bus_Routes (origin, destination, distance_km) VALUES 
            ('Kochi', 'Thiruvananthapuram', 200.00), 
            ('Kozhikode', 'Kannur', 92.00), 
            ('Ernakulam', 'Palakkad', 110.00), 
            ('Thrissur', 'Kottayam', 75.00), 
            ('Alappuzha', 'Kollam', 85.00); 
        ''')
        connection.commit()

def show_login_interface():
    """ Create the login interface. """
    for widget in main_frame.winfo_children():
        widget.destroy()

    title_label = ctk.CTkLabel(main_frame, text="Welcome to Bus Booking System", font=("Arial", 24))
    title_label.pack(pady=10)

    email_label = ctk.CTkLabel(main_frame, text="Email:")
    email_label.pack(pady=5)
    email_entry = ctk.CTkEntry(main_frame)
    email_entry.pack(pady=5)

    password_label = ctk.CTkLabel(main_frame, text="Password:")
    password_label.pack(pady=5)
    password_entry = ctk.CTkEntry(main_frame, show='*')
    password_entry.pack(pady=5)

    # Enhanced blue color for the Login button
    login_button = ctk.CTkButton(main_frame, text="Login", fg_color="#4682B4", hover_color="#3A5F7A",
                                 command=lambda: login(email_entry.get(), password_entry.get()))
    login_button.pack(pady=10)

    register_button = ctk.CTkButton(main_frame, text="Register", fg_color="gray", command=show_registration_interface)
    register_button.pack(pady=5)

def show_registration_interface():
    """ Create the registration interface. """
    for widget in main_frame.winfo_children():
        widget.destroy()

    title_label = ctk.CTkLabel(main_frame, text="Register", font=("Arial", 24))
    title_label.pack(pady=10)

    name_label = ctk.CTkLabel(main_frame, text="Name:")
    name_label.pack(pady=5)
    name_entry = ctk.CTkEntry(main_frame)
    name_entry.pack(pady=5)

    email_label = ctk.CTkLabel(main_frame, text="Email:")
    email_label.pack(pady=5)
    email_entry = ctk.CTkEntry(main_frame)
    email_entry.pack(pady=5)

    phone_label = ctk.CTkLabel(main_frame, text="Phone Number:")
    phone_label.pack(pady=5)
    phone_entry = ctk.CTkEntry(main_frame)
    phone_entry.pack(pady=5)

    password_label = ctk.CTkLabel(main_frame, text="Password:")
    password_label.pack(pady=5)
    password_entry = ctk.CTkEntry(main_frame, show='*')
    password_entry.pack(pady=5)

    register_button = ctk.CTkButton(main_frame, text="Register", fg_color="gray", command=lambda: register(name_entry.get(), email_entry.get(), phone_entry.get(), password_entry.get()))
    register_button.pack(pady=10)

def register(name, email, phone, password):
    try:
        dbcon(f"INSERT INTO Users (name, email, phone_number, password) VALUES ('{name}', '{email}', '{phone}', '{password}')",0)
        messagebox.showinfo("Registration Successful", "You can now log in.")
        show_login_interface()
    except sqlite3.IntegrityError:
        messagebox.showwarning("Registration Failed", "Email already exists.")

def login(email, password):
    email = '1234'
    password = '1234'
    dbcon(f"select * from users where email='{email}' and password = '{password}'",1)
    
    if len(resultArr) != 0:
        global current_user
        current_user = resultArr[0][0]  # Store user ID for later use
        show_main_menu()
    else:
        messagebox.showwarning("Login Failed", "Invalid email or password.")

def show_main_menu():
    """ Show the main menu after logging in. """
    for widget in main_frame.winfo_children():
        widget.destroy()

    title_label = ctk.CTkLabel(main_frame, text="Main Menu", font=("Arial", 24))
    title_label.pack(pady=10)

    routes_button = ctk.CTkButton(main_frame, text="View Available Routes", command=show_routes_page)
    routes_button.pack(pady=5)

    bookings_button = ctk.CTkButton(main_frame, text="View My Bookings", command=view_bookings)
    bookings_button.pack(pady=5)

    # Enhanced red color for the Logout button
    logout_button = ctk.CTkButton(main_frame, text="Logout", fg_color="#C0392B", hover_color="#A93226",
                                  command=logout)
    logout_button.pack(pady=5)


def show_routes_page():
    """ Show the available routes with a back button. """
    for widget in main_frame.winfo_children():
        widget.destroy()

    title_label = ctk.CTkLabel(main_frame, text="Available Routes", font=("Arial", 24))
    title_label.pack(pady=10)

    cursor.execute("SELECT * FROM Bus_Routes")
    routes = cursor.fetchall()

    for route in routes:
        route_button = ctk.CTkButton(main_frame, text=f"{route[1]} to {route[2]} (Distance: {route[3]} km)",
                                      command=lambda r_id=route[0]: go_to_booking_page(r_id))
        route_button.pack(pady=5)

    # Enhanced red color for Back button
    back_button = ctk.CTkButton(main_frame, text="Back to Main Menu", fg_color="#C0392B", hover_color="#A93226",
                                command=show_main_menu)
    back_button.pack(pady=10)

def go_to_booking_page(route_id):
    for widget in main_frame.winfo_children():
        widget.destroy()

    title_label = ctk.CTkLabel(main_frame, text="Available Buses", font=("Arial", 24))
    title_label.pack(pady=10)

    dbcon(f"SELECT bus_id, bus_type, fare, seats_available FROM Bus_Details WHERE route_id = {route_id}", 1)

    for bus in resultArr:
        bus_id, bus_type, fare, seats_left = bus

        bus_label = ctk.CTkLabel(main_frame, text=f"{bus_type} - Fare: ₹{fare} - Seats Left: {seats_left}")
        bus_label.pack(pady=5)

        if seats_left > 0:
            book_button = ctk.CTkButton(main_frame, text="Book Now", command=lambda b_id=bus_id: book_seat(b_id))
            book_button.pack(pady=5)
        else:
            sold_out_label = ctk.CTkLabel(main_frame, text="Sold Out", fg_color="red")
            sold_out_label.pack(pady=5)

    # Back button, now red
    back_button = ctk.CTkButton(main_frame, text="Back to Routes", fg_color="#D9534F", hover_color="#B52A28",
                                command=show_routes_page)
    back_button.pack(pady=10)

def book_seat(bus_id):
    
    dbcon(f"SELECT seats_available FROM Bus_Details WHERE bus_id = {bus_id}", 1)
    seats_available = resultArr[0][0]

    if seats_available > 0:
        # Insert booking into the Bookings table
        booking_date = date.today()
        seat_number = seats_available 


        dbcon(f"UPDATE Bus_Details SET seats_available = seats_available - 1 WHERE bus_id = {bus_id}", 0)

        dbcon(f"INSERT INTO Bookings (user_id, bus_id, booking_date, seat_number) VALUES ({current_user}, {bus_id}, '{booking_date}', {seat_number})",0)

        messagebox.showinfo("Booking Confirmed", "Your seat has been booked successfully!")
        show_main_menu()
    else:
        messagebox.showwarning("Booking Failed", "No seats available.")

def view_bookings():
    for widget in main_frame.winfo_children():
        widget.destroy()

    title_label = ctk.CTkLabel(main_frame, text="My Bookings", font=("Arial", 24))
    title_label.pack(pady=10)

    dbcon("SELECT A.booking_id, A.bus_id, A.booking_date, A.seat_number, B.bus_type,C.origin,C.destination FROM bookings A,bus_details B,bus_routes C where A.bus_id = B.bus_id and B.route_id = C.route_id",1)

    if len(resultArr) != 0:
        for booking in resultArr:
            booking_label = ctk.CTkLabel(main_frame, text=f"Booking ID: {booking[0]} - {booking[1]} - {booking[2]} to {booking[3]} - Date: {booking[4]} - Seat: {booking[5]}")
            booking_label.pack(pady=5)

            delete_button = ctk.CTkButton(main_frame, text="Delete", fg_color="red", command=lambda b_id=booking[0], bus_id=booking[1]: delete_booking(b_id, bus_id))
            delete_button.pack(pady=5)

    # Enhanced red color for Back button
    back_button = ctk.CTkButton(main_frame, text="Back to Menu", fg_color="#C0392B", hover_color="#A93226",
                                command=show_main_menu)
    back_button.pack(pady=10)

def delete_booking(booking_id, bus_id):
    try:
        # Retrieve current available seats for the bus
        dbcon(f"SELECT seats_available FROM Bus_Details WHERE bus_id = {bus_id}", 1)
        if len(resultArr) == 0:
            messagebox.showwarning("Update Failed", "Bus not found.")
            return
        
        # Current available seats
        seats_available = resultArr[0][0]

        # Delete the booking from the Bookings table
        dbcon(f"DELETE FROM Bookings WHERE booking_id = {booking_id}", 0)

        # Increment the available seats count for the bus
        new_seats_available = seats_available + 1
        dbcon(f"UPDATE Bus_Details SET seats_available = {new_seats_available} WHERE bus_id = {bus_id}", 0)

        # Confirmation message
        messagebox.showinfo("Booking Deleted", "Your booking has been deleted!")
        
        # Refresh the bookings view to reflect changes
        view_bookings()

    except Exception as e:
        # Handle any errors that occur
        messagebox.showerror("Error", f"An error occurred: {e}")


def logout():
    global current_user
    current_user = None
    show_login_interface()

# Database setup
connection = create_connection()
cursor = connection.cursor()
create_tables(cursor)
insert_default_data(cursor)

# Tkinter UI setup
app = ctk.CTk()
app.geometry("600x700")
app.title("Bus Booking System")

main_frame = ctk.CTkFrame(app)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

current_user = None
show_login_interface()
app.mainloop()

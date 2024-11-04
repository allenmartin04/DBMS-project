import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector

def database_connection():
    return mysql.connect(
        host='localhost',
        user='root',
        password='1999', 
        database='bus_booking'
    )

# Initialize customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BusBookingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure main window
        self.title("Bus Booking System")
        self.geometry("500x600")

        # Create frames for login, sign-up, and booking
        self.login_frame = ctk.CTkFrame(self, width=300, height=300, corner_radius=10)
        self.signup_frame = ctk.CTkFrame(self, width=300, height=350, corner_radius=10)
        self.booking_frame = ctk.CTkFrame(self, corner_radius=15)
        self.bus_list_frame = None

        self.show_login_interface()  # Show login interface initially

    def show_login_interface(self):
        # Clear and pack the login interface
        self.signup_frame.pack_forget()
        self.booking_frame.pack_forget()
        if self.bus_list_frame:
            self.bus_list_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Initialize login frame widgets
        for widget in self.login_frame.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self.login_frame, text="Login", font=("Arial", 24))
        title_label.pack(pady=10)

        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Username", width=200)
        self.username_entry.pack(pady=(20, 10))

        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*", width=200)
        self.password_entry.pack(pady=10)

        login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login)
        login_button.pack(pady=10)

        signup_button = ctk.CTkButton(self.login_frame, text="Sign Up", command=self.show_signup_interface, fg_color="gray")
        signup_button.pack(pady=10)

    def show_signup_interface(self):
        self.login_frame.pack_forget()
        self.signup_frame.pack(fill="both", expand=True, padx=20, pady=20)

        for widget in self.signup_frame.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self.signup_frame, text="Sign Up", font=("Arial", 24))
        title_label.pack(pady=10)

        self.name_entry = ctk.CTkEntry(self.signup_frame, placeholder_text="Full Name", width=200)
        self.name_entry.pack(pady=(10, 10))

        self.signup_username_entry = ctk.CTkEntry(self.signup_frame, placeholder_text="Username", width=200)
        self.signup_username_entry.pack(pady=10)

        self.email_entry = ctk.CTkEntry(self.signup_frame, placeholder_text="Email", width=200)
        self.email_entry.pack(pady=10)

        self.signup_password_entry = ctk.CTkEntry(self.signup_frame, placeholder_text="Password", show="*", width=200)
        self.signup_password_entry.pack(pady=10)

        signup_button = ctk.CTkButton(self.signup_frame, text="Create Account", command=self.signup)
        signup_button.pack(pady=10)

        back_to_login_button = ctk.CTkButton(self.signup_frame, text="Back to Login", command=self.show_login_interface, fg_color="gray")
        back_to_login_button.pack(pady=10)

    def create_booking_frame(self):
        for widget in self.booking_frame.winfo_children():
            widget.destroy()

        from_label = ctk.CTkLabel(self.booking_frame, text="Boarding From", font=("Arial", 14))
        from_label.pack(pady=(20, 5))

        self.from_entry = ctk.CTkEntry(self.booking_frame, placeholder_text="Enter boarding location", width=250)
        self.from_entry.pack(pady=5)

        to_label = ctk.CTkLabel(self.booking_frame, text="Where are you going?", font=("Arial", 14))
        to_label.pack(pady=(20, 5))

        self.to_entry = ctk.CTkEntry(self.booking_frame, placeholder_text="Enter destination", width=250)
        self.to_entry.pack(pady=5)

        date_label = ctk.CTkLabel(self.booking_frame, text="Select Date", font=("Arial", 14))
        date_label.pack(pady=(20, 5))

        self.date_entry = DateEntry(self.booking_frame, width=18, background="orange", foreground="black", borderwidth=2)
        self.date_entry.pack(pady=5)

        find_button = ctk.CTkButton(self.booking_frame, text="Find Bus", command=self.show_bus_list, width=150, fg_color="orange")
        find_button.pack(pady=(20, 10))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = database_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE email = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Login Successful", "Welcome!")
            self.show_booking_frame()
        else:
            messagebox.showwarning("Login Failed", "Invalid credentials.")

    def show_booking_frame(self):
        self.login_frame.pack_forget()
        self.signup_frame.pack_forget()
        self.booking_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.create_booking_frame()

    def signup(self):
        name = self.name_entry.get()
        username = self.signup_username_entry.get()
        email = self.email_entry.get()
        password = self.signup_password_entry.get()

        if name and username and email and password:
            conn = database_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Users (name, email, phone_number, password) VALUES (%s, %s, %s, %s)", 
                               (name, email, username, password))
                conn.commit()
                messagebox.showinfo("Sign Up Successful", "Account created!")
                self.show_login_interface()
            except mysql.IntegrityError:
                messagebox.showwarning("Sign Up Failed", "Email already exists.")
            finally:
                conn.close()
        else:
            messagebox.showwarning("Sign Up Failed", "Please fill in all fields.")

    def show_bus_list(self):
        from_location = self.from_entry.get().strip()
        to_location = self.to_entry.get().strip()

        if not from_location or not to_location:
            messagebox.showwarning("Invalid Input", "Please enter both boarding and destination locations.")
            return

        self.booking_frame.pack_forget()
        if self.bus_list_frame:
            self.bus_list_frame.pack_forget()

        self.bus_list_frame = ctk.CTkFrame(self, corner_radius=10)
        self.bus_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        conn = database_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT bd.bus_type, bd.fare, bt.departure_time, bt.arrival_time FROM Bus_Details bd "
            "JOIN Bus_Routes br ON bd.route_id = br.route_id "
            "JOIN Bus_Timings bt ON bt.route_id = br.route_id "
            "WHERE br.origin = %s AND br.destination = %s", 
            (from_location, to_location)
        )
        buses = cursor.fetchall()
        conn.close()

        route_text = f"Selected Route: {from_location} to {to_location}"
        date_text = f"Date: {self.date_entry.get_date()}"
        
        route_label = ctk.CTkLabel(self.bus_list_frame, text=route_text, font=("Arial", 16))
        route_label.pack(pady=(10, 2))

        date_label = ctk.CTkLabel(self.bus_list_frame, text=date_text, font=("Arial", 14), fg_color="gray")
        date_label.pack()

        for bus in buses:
            bus_info = {
                "name": "Bus",
                "type": bus[0],
                "time": f"{bus[2]} - {bus[3]}",
                "seats": "Available",  # Placeholder as seats data isn't defined
                "price": str(bus[1])
            }
            self.create_bus_card(bus_info)

    def create_bus_card(self, bus):
        bus_frame = ctk.CTkFrame(self.bus_list_frame, corner_radius=10, fg_color="lightgray", height=100)
        bus_frame.pack(fill="x", pady=5, padx=5)

        bus_info = f"{bus['name']} - {bus['type']}"
        bus_name_label = ctk.CTkLabel(bus_frame, text=bus_info, font=("Arial", 14, "bold"))
        bus_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        time_label = ctk.CTkLabel(bus_frame, text=f"Time: {bus['time']}", font=("Arial", 12))
        time_label.grid(row=1, column=0, padx=10, sticky="w")

        seats_label = ctk.CTkLabel(bus_frame, text=f"Seats Left: {bus['seats']}", font=("Arial", 12))
        seats_label.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")

        price_button = ctk.CTkButton(bus_frame, text=f"${bus['price']}", fg_color="green", width=80, height=40)
        price_button.grid(row=0, column=1, rowspan=3, padx=20, pady=10, sticky="e")

# Run the application
if __name__ == "__main__":
    app = BusBookingApp()
    app.mainloop()

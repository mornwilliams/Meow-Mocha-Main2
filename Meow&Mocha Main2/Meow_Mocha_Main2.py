from dataclasses import dataclass, field # For data classes including Customer, Staff, TimeSlot, and Booking
from datetime import date, datetime, time, timedelta # For handling dates, times, and durations, especially for bookings and time slots
import csv # For reading and writing time slot and booking data in CSV format
import pickle # For saving and loading customer and staff data in binary format, this allows me to save and load customer and staff objects with all their attributes
import os # For checking if data files exist before trying to load them
import tkinter as tk # Tkinter GUI module for building my application's graphical user interface, including windows, buttons, labels, and entry fields
from tkinter import SE, Entry, Frame, messagebox, Image, PhotoImage, ttk, simpledialog
from typing import Optional # For type hinting, allowing me to specify that certain functions may return a Customer, Staff, or None
from tkcalendar import Calendar, DateEntry #Calendar widget and date entry widget for selecting dates in the GUI


#-- Password hashing

def hashPassword(plain:str) -> str:
    return plain[::-1]  #placeholder (not plain text)

def verifyPassword(plain:str, hashed:str) -> bool:
    return hashPassword(plain) == hashed

#  Date time conversions here
def parseDate(date_str: str) -> date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def parseTime(time_str: str) -> time:
    return datetime.strptime(time_str, "%H:%M").time()

def formatDate(date_obj: date) -> str:
    return date_obj.strftime("%Y-%m-%d")

def formatTime(time_obj: time) -> str:
    return time_obj.strftime("%H:%M")

def parseTimeStamp(timestamp_str: str) -> datetime:
    return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

def formatTimeStamp(timestamp_obj: datetime) -> str:
    return timestamp_obj.strftime("%Y-%m-%d %H:%M:%S")

# ---- Data classes for: Customer, Staff, TimeSlot, Booking ----

@dataclass
class Customer:
    customer_id: str
    first_name: str
    surname:str
    date_of_birth: date
    email:str
    phone_number:str
    password_hash:str

    def editFirstName(self, new_first_name: str) -> None:
        self.first_name = new_first_name
    def editSurname(self, new_surname: str) -> None:
        self.surname = new_surname
    def editDateOfBirth(self, new_dob: date) -> None:
        self.date_of_birth = new_dob
    def editEmail(self, new_email: str) -> None:
        self.email = new_email
    def editPhoneNumber(self, new_phone_number:str) -> None:
        self.phone_number = new_phone_number

    def setPassword(self, plain_password: str) -> None:
        self.password_hash = hashPassword(plain_password)

@dataclass
class Staff:
    staff_id: str
    first_name: str
    surname:str
    date_of_birth: date
    email:str
    phone_number:str
    password_hash:str
    higher_admin:bool

    #editing methods here
    def editFirstName(self, new_first_name: str) -> None:
        self.first_name = new_first_name
    def editSurname(self, new_surname: str) -> None:
        self.surname = new_surname
    def editDateOfBirth(self, new_dob: date) -> None:
        self.date_of_birth = new_dob
    def editEmail(self, new_email: str) -> None:
        self.email = new_email
    def editPhoneNumber(self, new_phone_number:str) -> None:
        self.phone_number = new_phone_number

    def setPassword(self, plain_password: str) -> None:
        self.password_hash = hashPassword(plain_password)

@dataclass
class TimeSlot:
    timeslot_id: str
    date: date
    start_time: time
    end_time: time
    max_capacity: int
    is_available: bool=True

    #duration method here, returns timedelta 
    def duration(self) -> timedelta:
        dt_start = datetime.combine(self.date, self.start_time)
        dt_end = datetime.combine(self.date, self.end_time)
        return dt_end - dt_start

@dataclass
class Booking:  
    booking_id: str
    customer_id: str
    timeslot_id: str
    number_of_guests: int
    status: str #such as "BOOKED", "CANCELLED", "COMPLETED"           
    booking_timestamp: datetime = field(default_factory=datetime.now)

    #cancel method here
    def cancelBooking(self):
        if self.status == "BOOKED":
            self.status = "CANCELLED"

    #complete method here
    def completeBooking(self):
        if self.status == "BOOKED":
            self.status = "COMPLETED"

#---- System manager with methods properly defined inside the class ----

class SystemManager:
    def __init__(self) -> None:
        # data containers
        self.customers: list[Customer] = []
        self.staff: list[Staff] = []
        self.timeslots: list[TimeSlot] = []
        self.bookings: list[Booking] = []

        # id counters
        self.next_customer_id: int = 1
        self.next_staff_id: int = 1
        self.next_timeslot_id: int = 1
        self.next_booking_id: int = 1

    # ID generators
    def generateCustomerID(self) -> str:
        cID = f"C{self.next_customer_id:05d}"
        self.next_customer_id += 1
        return cID

    def generateStaffID(self) -> str:   
        sID = f"S{self.next_staff_id:05d}"
        self.next_staff_id += 1
        return sID

    def generateTimeSlotID(self) -> str:
        tID = f"T{self.next_timeslot_id:05d}"
        self.next_timeslot_id += 1
        return tID

    def generateBookingID(self) -> str:
        bID = f"B{self.next_booking_id:05d}"
        self.next_booking_id += 1
        return bID

    def validateCommonRegistration(self, firstname, surname, email, phonenumber, dob, password):
        if not firstname.strip():
            return "Please enter first name"

        if not surname.strip():
            return "Please enter surname"

        if not email.strip():
            return "Please enter email"

        if "@" not in email:
            return "Email must contain '@'"

        if not phonenumber.strip():
            return "Please enter phone number"

        if not phonenumber.isdigit():
            return "Phone number must contain digits only"

        if len(phonenumber) < 11:
            return "Phone number must be at least 11 digits"

        if not password:
            return "Please enter a password"

        if len(password) < 8:
            return "Password must be at least 8 characters"

        if dob is None:
            return "Please enter date of birth"

        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 16:
            return "You must be at least 16 years old to create an account"

        return ""


    # load / save 
    def loadData(self) -> None:
        self._load_customers()
        self._load_staff()
        self._load_timeslots()
        self._load_bookings()

    def saveData(self) -> None:
        self._save_customers()  
        self._save_staff()
        self._save_timeslots()
        self._save_bookings()

    # internal IO implementations (consistent naming)
    def _load_customers(self) -> None:
        if os.path.exists("customers.pkl"):
            with open("customers.pkl", "rb") as f:
                self.customers = pickle.load(f)
            # set next customer id
            if self.customers:
                max_id_num = max(int(c.customer_id[1:]) for c in self.customers)
                self.next_customer_id = max_id_num + 1
            self.customers.sort(key=lambda c: c.email)

    def _save_customers(self) -> None:
        with open("customers.pkl", "wb") as f:
            pickle.dump(self.customers, f)

    def _load_staff(self) -> None:
        if os.path.exists("staff.pkl"):
            with open("staff.pkl", "rb") as f:
                self.staff = pickle.load(f)
            # set next staff id
            if self.staff:
                max_id_num = max(int(s.staff_id[1:]) for s in self.staff)
                self.next_staff_id = max_id_num + 1
            self.staff.sort(key=lambda s: s.email)

    def _save_staff(self) -> None:
        with open("staff.pkl", "wb") as f:
            pickle.dump(self.staff, f)

    def _load_timeslots(self) -> None:
        self.timeslots = []
        if not os.path.exists("timeslots.csv"):
            return
        with open("timeslots.csv", "r", newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                timeslot = TimeSlot(
                    timeslot_id=row["timeslot_id"],
                    date=parseDate(row["date"]),
                    start_time=parseTime(row["start_time"]),
                    end_time=parseTime(row["end_time"]),
                    max_capacity=int(row["max_capacity"]),
                    is_available=row.get("is_available", "True").lower() == "true"
                )
                self.timeslots.append(timeslot)
            # set next timeslot id
            if self.timeslots:
                max_id_num = max(int(t.timeslot_id[1:]) for t in self.timeslots)
                self.next_timeslot_id = max_id_num + 1

    def _save_timeslots(self) -> None:
        with open("timeslots.csv", "w", newline='', encoding="utf-8") as f:
            fieldnames = ["timeslot_id", "date", "start_time", "end_time", "max_capacity", "is_available"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for t in self.timeslots:
                writer.writerow({
                    "timeslot_id": t.timeslot_id,
                    "date": formatDate(t.date),
                    "start_time": formatTime(t.start_time),
                    "end_time": formatTime(t.end_time),
                    "max_capacity": t.max_capacity,
                    "is_available": str(t.is_available),
                })

    def _load_bookings(self) -> None:
        self.bookings = []
        if not os.path.exists("bookings.csv"):
            return
        with open("bookings.csv", "r", newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                booking = Booking(
                    booking_id=row["booking_id"],
                    customer_id=row["customer_id"],
                    timeslot_id=row["timeslot_id"],
                    number_of_guests=int(row["number_of_guests"]),
                    status=row["status"],
                    booking_timestamp=parseTimeStamp(row["booking_timestamp"])
                )
                self.bookings.append(booking)
            # set next booking id    
            if self.bookings:
                max_id_num = max(int(b.booking_id[1:]) for b in self.bookings)
                self.next_booking_id = max_id_num + 1

    def _save_bookings(self) -> None:
        with open("bookings.csv", "w", newline='', encoding="utf-8") as f:
            fieldnames = ["booking_id", "customer_id", "timeslot_id", "number_of_guests", "status", "booking_timestamp"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for b in self.bookings:
                writer.writerow({
                    "booking_id": b.booking_id,
                    "customer_id": b.customer_id,
                    "timeslot_id": b.timeslot_id,
                    "number_of_guests": b.number_of_guests,
                    "status": b.status,
                    "booking_timestamp": formatTimeStamp(b.booking_timestamp),
                })

    # ----- Lookups and searches (binary search expects sorted lists)

    def findCustomerByEmail(self, email: str) -> Optional[Customer]:
        target = email.lower()
        left = 0
        right = len(self.customers) - 1

        while left <= right:
            mid = (left + right) // 2
            mid_email = self.customers[mid].email.lower()

            if mid_email == target:
                return self.customers[mid]
            elif mid_email < target:
                left = mid + 1
            else:
                right = mid - 1

        return None

    def findStaffByEmail(self, email: str) -> Optional[Staff]:
        target = email.lower()
        left = 0
        right = len(self.staff) - 1
        while left <= right:
            mid = (left + right) // 2
            mid_email = self.staff[mid].email.lower()
            if mid_email == target:
                return self.staff[mid]
            elif mid_email < target:
                left = mid + 1
            else:
                right = mid - 1
        return None

    # ---- Registering and logging in users here --

    def registerCustomer(self, firstname, surname, dateofbirth, email, phonenumber, plainpassword):
        if self.findCustomerByEmail(email) or self.findStaffByEmail(email):
            raise ValueError("Email already in use")

        error = self.validateCommonRegistration(firstname, surname, email, phonenumber, dateofbirth, plainpassword)
        if error:
            raise ValueError(error)

        customerid = self.generateCustomerID()
        passwordhash = hashPassword(plainpassword)

        newcustomer = Customer(
            customer_id=customerid,
            first_name=firstname.strip(),
            surname=surname.strip(),
            date_of_birth=dateofbirth,
            email=email.strip().lower(),
            phone_number=phonenumber.strip(),
            password_hash=passwordhash
        )

        self.customers.append(newcustomer)
        self.customers.sort(key=lambda c: c.email)
        return newcustomer


    def loginCustomer(self, email: str, plain_password: str) -> Optional[Customer]:
        found = self.findCustomerByEmail(email)
        if found and verifyPassword(plain_password, found.password_hash):
            return found
        return None

    def registerStaff(self, firstname, surname, dateofbirth, email, phonenumber, plainpassword, higheradmin):
        if self.findStaffByEmail(email) or self.findCustomerByEmail(email):
            raise ValueError("Email already in use")

        error = self.validateCommonRegistration(firstname, surname, email, phonenumber, dateofbirth, plainpassword)
        if error:
            raise ValueError(error)

        staffid = self.generateStaffID()
        passwordhash = hashPassword(plainpassword)

        newstaff = Staff(
            staffid=staffid,
            firstname=firstname.strip(),
            surname=surname.strip(),
            dateofbirth=dateofbirth,
            email=email.strip().lower(),
            phonenumber=phonenumber.strip(),
            passwordhash=passwordhash,
            higheradmin=higheradmin
        )

        self.staff.append(newstaff)
        self.staff.sort(key=lambda s: s.email)
        return newstaff


    def loginStaff(self, email: str, plain_password: str) -> Optional[Staff]:
        found = self.findStaffByEmail(email)
        if found and verifyPassword(plain_password, found.password_hash):
            return found
        return None

    #  ------ Time slot and capacity management ------

    def currentGuestsInTimeslot(self, timeslot_id: str) -> int:
        total_guests = 0
        for booking in self.bookings:
            if booking.timeslot_id == timeslot_id and booking.status == "BOOKED":
                total_guests += booking.number_of_guests
        return total_guests

    def isTimeSlotFull(self, ts: TimeSlot) -> bool:
        return self.currentGuestsInTimeslot(ts.timeslot_id) >= ts.max_capacity

    def recalculateTimeSlotAvailability(self, ts: TimeSlot) -> None:
        ts.is_available = not self.isTimeSlotFull(ts)

    # ---- Booking management -----

    def createBooking(self, customer: Customer, timeslot: TimeSlot, number_of_guests: int) -> Booking:
        if not timeslot.is_available:
            raise ValueError("Time slot is not available")
        if self.currentGuestsInTimeslot(timeslot.timeslot_id) + number_of_guests > timeslot.max_capacity:
            raise ValueError("Not enough capacity in the selected time slot")

        current = self.currentGuestsInTimeslot(timeslot.timeslot_id)
        if current + number_of_guests >= timeslot.max_capacity:
            raise ValueError("Booking would exceed time slot capacity")

        booking_id = self.generateBookingID()
        new_booking = Booking(
            booking_id=booking_id,
            customer_id=customer.customer_id,
            timeslot_id=timeslot.timeslot_id,
            number_of_guests=number_of_guests,
            status="BOOKED"
        )
        self.bookings.append(new_booking)
        self.recalculateTimeSlotAvailability(timeslot)
        return new_booking

    def cancelBooking(self, booking: Booking) -> None:
        booking.cancelBooking()
        # updates timeslot availability
        timeslot = next((ts for ts in self.timeslots if ts.timeslot_id == booking.timeslot_id), None)
        if timeslot:
            self.recalculateTimeSlotAvailability(timeslot)

# ---- GUI classes and functions here ----

class MeowMochaApp:
    def __init__(self, root: tk.Tk, system: SystemManager):
        self.root = root
        self.system = system
        self.root.configure(bg = "#ffc4df"  ) #pink background 
        self.root.title("Meow&Mocha System")
        self.root.minsize(1000, 650)  

        self.logo_image = tk.PhotoImage(file="MM3.png")
        self.account_image= tk.PhotoImage(file="accounticon.png")
        self.search_image= tk.PhotoImage(file="search.png")
        # load data from the system manager 
        self.system.loadData()
        self.testStaffAccount()
        self.current_frame = None
        self.showMainMenu()


    def addExitButton(self, frame: tk.Frame):
        tk.Button(
            frame,
            text="Exit",
            font=("Helvetica", 12),
            command=self.root.destroy,   
        ).pack(side="bottom", anchor="e", padx=10, pady=10)

    #  ----- Test data creation (for staff accounts) ----

    def testStaffAccount(self):
        test_email = "staff@test.com"
        test_admin_email = "admin@test.com"
        existing = self.system.findStaffByEmail(test_email)
        if existing is not None:
            return

        self.system.registerStaff( # creating a test staff account with email "
            first_name="Test",
            surname="Staff",
            date_of_birth=parseDate("1990-01-01"),
            email=test_email,
            phone_number="1234567890",
            plain_password="password123",
            higher_admin=False
        )

        self.system.registerStaff( #creates a test higher admin account with email "
            first_name="Test",
            surname="Admin",
            date_of_birth=parseDate("1990-01-01"),
            email=test_admin_email,
            phone_number="1234567890",
            plain_password="password123",
            higher_admin=True
        )
        self.system.saveData() #save data after creating test account

    def show_frame (self, builder_function, *args): # to show any frame based on the builder function provided, destroys current frame if it exists, creates new frame, adds logo, and calls the builder function to populate the frame
        if self.current_frame is not None:
            self.current_frame.destroy()
        
        frame = tk.Frame(self.root, bg ="#FFFFFF")
        self.logo_image = tk.PhotoImage(file="MM3.png")
        self.logo_image_small = self.logo_image.subsample(2, 2)
        logo_label = tk.Label(frame, image=self.logo_image_small, bg="#ffffff")
        logo_label.image = self.logo_image_small  
        logo_label.pack(side="top", anchor="w", padx=10, pady=10)


        frame.pack(padx=20, pady=10,fill="both", expand=True )
        self.current_frame = frame

        builder_function(frame, *args) # Populates the frame based on the builder function provided (e.g., main menu, login page, etc.)
   
       
    def showMainMenu(self):
        self.show_frame(self.build_main_menu)

    def build_main_menu(self, frame: tk.Frame):
       
        
        tk.Label(
            frame,
            text = "Welcome to Meow&Mocha!",
            font = ("Helvetica", 20, "bold"),
            bg = "#ffffff",
        ).pack(pady=30)

        tk.Button(
            frame,
            text="Customer Portal",
            font = ("Helvetica", 16),
            width=20,
            command = self.showCustomerLogIn
        ).pack(pady=5)
        tk.Button(
            frame,
            text="Staff Portal",
            font = ("Helvetica", 16),
            width=20,
            command= self.showStaffLogIn
        ).pack(pady=5)#
        

    # ──────  Customer Portals fpr LOG IN and SIGN UP here ───────────

    def showCustomerLogIn(self):
        self.show_frame(self.buildCustomerLogInPortal)

    def buildCustomerLogInPortal(self, frame: tk.Frame): 
        tk.Label(
            frame,
            text="Customer Login",
            font=("Helvetica", 20, "bold"),
            bg="#ffffff",
        ).pack(pady=10)

        form = tk.Frame(frame, bg="#ffffff")
        form.pack(pady=10)  #A sub frame so a grid can be used for the form entries

        tk.Label(form,font = ("Helvetica", 12), text="Email:", bg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        email_entry = tk.Entry(form, width=30)
        email_entry.grid(row=0, column=1, padx=5, pady=5,)

        tk.Label(form,font = ("Helvetica", 12), text="Password:", bg="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        password_entry = tk.Entry(form, show="*", width=30)
        password_entry.grid(row=1, column=1, padx=5, pady=5,)

        tk.Button(
            frame,
            text="Log in",
            font=("Helvetica", 14, "bold"),
            command=lambda: self.handle_customer_login(email_entry.get(),
                                                       password_entry.get()),
        ).pack(pady=20)

        tk.Label(
            frame,
            text="Not a Customer yet?",
            font=("Helvetica", 10),
            bg="#ffffff",
        ).pack(pady=5)

        tk.Button(
            frame,
            text="Sign up",
            font=("Helvetica", 14, "bold"),
            command= self.showCustomerSignUp
        ).pack(pady=5)


        tk.Button(
            frame,
            text="Back",
            command=self.showMainMenu,
            font = ("Helvetica", 12),
        ).pack (side= "bottom" , anchor="w",padx= 10, pady=10)

    def handle_customer_login(self, email: str, password: str):
        email = email.strip()
        password = password.strip()

        if not email or not password:
            messagebox.showerror("Log in error", "Please enter both email and password.")
            return
        
        customer = self.system.loginCustomer(email, password)
        if customer is None:
            messagebox.showerror("Log in error", "Invalid email or password.")
            return

       
        self.showCustomerHub(customer)

    # ---- Customer sign up portal and handling here ----

    def showCustomerSignUp(self):

        self.show_frame(self.buildCustomerSignUpPortal)

    def buildCustomerSignUpPortal(self, frame: tk.Frame):
        tk.Label(
            frame,
            text="Customer Sign up",
            font=("Helvetica", 20, "bold"),
            bg="#ffffff",
        ).pack(pady=20)

        form = tk.Frame(frame, bg="#ffffff") #A sub frame so a grid can be used for the form entries
        form.pack(pady=20)

        # Entries for first name, surname, dob, email, phone number, password
        tk.Label(
            form,
            text="First Name:",
            font=("Helvetica", 12),
            bg="#ffffff",
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        firstname_entry = tk.Entry(form, width=30)
        firstname_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            form,
            text="Surname:",
            font=("Helvetica", 12),
            bg="#ffffff",
        ).grid(row=1, column=0, sticky="w", padx=5, pady=5)

        surname_entry = tk.Entry(form, width=30)
        surname_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(
            form,
            text="E-mail:",
            font=("Helvetica", 12),
            bg="#ffffff",
        ).grid(row=2, column=0, sticky="w", padx=5, pady=5)

        email_entry = tk.Entry(form, width=30)
        email_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(
            form,
            text="Password:",
            font=("Helvetica", 12),
            bg="#ffffff",
        ).grid(row=3, column=0, sticky="w", padx=5, pady=5)

        password_entry = tk.Entry(form, width=30, show="*")
        password_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(
            form,
            text="Repeat password:",
            font=("Helvetica", 12),
            bg="#ffffff",
        ).grid(row=4, column=0, sticky="w", padx=5, pady=5)

        repeatpassword_entry = tk.Entry(form, width=30, show="*")
        repeatpassword_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(
            form,
            text="Date of Birth (YYYY-MM-DD):",
            font=("Helvetica", 12),
            bg="#ffffff",
        ).grid(row=5, column=0, sticky="w", padx=5, pady=5)

        dob_entry = tk.Entry(form, width=30)
        dob_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(
            form,
            text="Phone Number:",
            font=("Helvetica", 12),
            bg="#ffffff",
        ).grid(row=6, column=0, sticky="w", padx=5, pady=5)

        phone_entry = tk.Entry(form, width=30)
        phone_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(
            frame,
            text="Sign up",
            command=lambda: self.handleCustomerSignUp(
                firstname_entry.get(),
                surname_entry.get(),
                email_entry.get(),
                password_entry.get(),
                repeatpassword_entry.get(),
                dob_entry.get(),
                phone_entry.get()
                ),
        ).pack(pady=10)

        tk.Button(
            frame,
            text="Back",
            command=self.showCustomerLogIn,
            font = ("Helvetica", 12),
        ).pack (side= "bottom" , anchor="w",padx= 10, pady=10)

    # ----- Staff log in portal and handling here -----

    def showStaffLogIn(self):
        self.show_frame(self.buildStaffLogInPortal)

    def buildStaffLogInPortal(self, frame: tk.Frame):
        tk.Label(
            frame,
            text="Staff Log in",
            font=("Helvetica", 16, "bold"),
            bg="#ffffff",
        ).pack(pady=35)

        form = tk.Frame(frame, bg="#ffffff")
        form.pack(pady=10)  

        tk.Label(form,font = ("Helvetica", 12), text="Email:", bg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        email_entry = tk.Entry(form, width=30)
        email_entry.grid(row=0, column=1, padx=5, pady=5,)

        tk.Label(form,font = ("Helvetica", 12), text="Password:", bg="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        password_entry = tk.Entry(form, show="*", width=30)
        password_entry.grid(row=1, column=1, padx=5, pady=5,)

        tk.Button(
            frame,
            text="Log in",
            command=lambda: self.handle_staff_login(email_entry.get(), password_entry.get()),
        ).pack(pady=10)

        tk.Button(
            frame,
            text="Back",
            command=self.showMainMenu,
            font = ("Helvetica", 12),
        ).pack (side= "bottom" , anchor="w",padx= 10, pady=10)

    # ------------- Customer sign up handling (validation, error messages, etc.) ------------

    def handleCustomerSignUp(self, firstname, surname, email, password, repeatpassword, dobstr, phone):
        firstname = firstname.strip()
        surname = surname.strip()
        email = email.strip()
        password = password.strip()
        repeatpassword = repeatpassword.strip()
        dobstr = dobstr.strip()
        phone = phone.strip()

        if not firstname or not surname or not email or not password or not repeatpassword or not dobstr or not phone:
            messagebox.showerror("Sign up error", "All fields are required.")
            return

        if password != repeatpassword:
            messagebox.showerror("Sign up error", "Passwords do not match.")
            return

        try:
            dob = parseDate(dobstr)
        except ValueError:
            messagebox.showerror("Sign up error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        try:
            self.system.registerCustomer(firstname, surname, dob, email, phone, password)
            self.system.saveData()
            messagebox.showinfo("Sign up successful", "Your account has been created. You can now log in.")
            self.showCustomerLogIn()
        except ValueError as e:
            messagebox.showerror("Sign up error", str(e))


    #   ------------  Staff login handling here  ------------    

    def handle_staff_login(self, email: str, password: str):
       email = email.strip()
       password = password.strip()

       if not email or not password:
          messagebox.showerror("Log in error", "Please enter both email and password.")
          return
    
       staff = self.system.loginStaff(email, password)
       if staff is None:
          messagebox.showerror("Log in error", "Invalid email or password.")
          return

       if staff.higher_admin:
              self.show_frame(self.adminHub, staff)
       else:
           self.show_frame(self.buildStaffHub, staff)
       

    #   ------------  Customer Hub here  ------------

    def showCustomerHub(self, customer: Customer):
        self.show_frame(self.buildCustomerHub, customer)

    def buildCustomerHub(self, frame:tk.Frame, customer: Customer):
        
        top_right = tk.Frame(frame, bg="#ffffff")
        top_right.pack(side="top", anchor="ne", padx=5, pady=5)
       
        
        tk.Label(
            top_right,
            text="MY ACCOUNT",
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
        ).pack(side="left", padx=(0, 8))

        account_button = tk.Button(
            top_right,
            text="Manage my account",
            image=self.account_image,
            font=("Helvetica", 14),
            command=lambda: self.manageAccountPage(customer),
        )
        account_button.pack(side="left")

        tk.Label(
            frame,
            text = "Welcome to Meow&Mocha!",
            font = ("Helvetica", 16, "bold"),
            bg = "#ffffff",
        ).pack(pady=10)

        tk.Button(
            frame,
            text = "Create a new booking",
            font = ("Helvetica", 14),
            command=lambda: self.showCustomerBookingPage(customer)
            ).pack(pady=5)

        tk.Button(
            frame,
            text="View my bookings",
            font=("Helvetica", 14),
            command=lambda: self.showCustomerViewBookingPage(customer),
        ).pack(pady=5)


        self.addExitButton(frame)

    #   ------------  Staff Hub here    ------------

    def showStaffHub(self, staff:Staff):
        self.show_frame(self.buildStaffHub, staff)

    def buildStaffHub(self, frame: tk.Frame, staff: Staff):
         
        top_right = tk.Frame(frame, bg="#ffffff")
        top_right.pack(side="top", anchor="ne", padx=5, pady=5)
       
        
        tk.Label(
            top_right,
            text="MY ACCOUNT",
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
        ).pack(side="left", padx=(0, 8))

        account_button = tk.Button(
            top_right,
            text="Manage my account",
            image=self.account_image,
            font=("Helvetica", 14),
            command=lambda: self.manageAccountPage(staff),
        )
        account_button.pack(side="left")
      
        tk.Label(
            frame,
            text=f"Staff hub – welcome, {staff.first_name}",
            font=("Helvetica", 16, "bold"),
            bg="#ffffff",
         ).pack(pady=10)

        tk.Button(
            frame,
            text="Create booking for customer",
            font=("Helvetica", 14),
            command=lambda: self.showStaffCreateBookingPage(staff),
         ).pack(pady=5)

        tk.Button(
            frame,
            text="View Customers",
            font=("Helvetica", 14),
            command=lambda: self.showViewCustomersPage(staff),
         ).pack(pady=5)

        tk.Button(
             frame,
             text="View Bookings",
             font=("Helvetica", 14),
             command = lambda: self.showStaffViewBookingspage(staff),
         ).pack(pady=5)

        self.addExitButton(frame)

    #   ------------  Customer Booking page ------------

    def showCustomerBookingPage(self, customer: Customer):
        self.show_frame(self.customerBookingPage, customer)
        
    def customerBookingPage(self, frame:tk.Frame, customer: Customer):
        tk.Label(
            frame,
            text="Make a Booking",
            font=("Helvetica", 20, "bold"),
            bg="#ffffff",
        ).pack(pady=10)

        # Calendar on the left
        cal_frame = tk.Frame(frame, bg="#ffffff")
        cal_frame.pack(side="left", padx=20, pady=10)

        tk.Label(
            cal_frame,
            text="Select date:",
            font=("Helvetica", 12, "bold"),
            bg="#ffffff",
        ).pack(anchor="w")

        self.booking_calendar = Calendar(
            cal_frame,
            selectmode="day",
            date_pattern="yyyy-mm-dd",   # matches parseDate
        )
        self.booking_calendar.pack(pady=5)

        # Right‑side controls
        right = tk.Frame(frame, bg="#ffffff")
        right.pack(side="left", padx=40, pady=10, fill="y")

        tk.Label(right, text="From:", font=("Helvetica", 12), bg="#ffffff")\
            .grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Label(right, text="To:", font=("Helvetica", 12), bg="#ffffff")\
            .grid(row=1, column=0, padx=5, pady=5, sticky="w")

        times = []
        for h in range(9, 16):      # this will create time slots from 9:00 to 16:30
            for m in (0, 30):
                times.append(f"{h:02d}:{m:02d}")
        times.append("16:00") #this makes 16:00 a valid end time, but not a start time

        self.from_combo = ttk.Combobox(right, values=times, width=10, state="readonly")
        self.from_combo.grid(row=0, column=1, padx=5, pady=5)
        self.to_combo = ttk.Combobox(right, values=times, width=10, state="readonly")
        self.to_combo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(right, text="Number of guests:", font=("Helvetica", 12), bg="#ffffff")\
                .grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.guests_spin = tk.Spinbox(right, from_=1, to=10, width=5) 
        self.guests_spin.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(
            right,
            text="Create Booking",
            font=("Helvetica", 14, "bold"),
            command=lambda: self.handleCreateBooking(customer),
        ).grid(row=3, column=0, columnspan=2, pady=20)

        tk.Button(
            frame,
            text="Back",
            font=("Helvetica", 12),
            command=lambda: self.showCustomerHub(customer),
        ).pack(side="bottom", anchor="w", padx=10, pady=10)

# ---------- Booking creation logic (validation, capacity checks, etc.) ----------

    def handleCreateBooking(self, customer: Customer):
        date_str = self.booking_calendar.get_date()  # 'YYYY-MM-DD'
        from_str = self.from_combo.get()
        to_str = self.to_combo.get()
        guests_str = self.guests_spin.get()

        # Basic validation
        if not (date_str and from_str and to_str and guests_str):
            messagebox.showerror("Error", "Please select date, start time, end time and number of guests.")
            return

        try:
            booking_date = parseDate(date_str)
            start_time = parseTime(from_str)
            end_time = parseTime(to_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format.")
            return

        if end_time <= start_time:
            messagebox.showerror("Error", "End time must be after start time.")
            return

        # Only allow 30 or 60 minutes
        delta = datetime.combine(booking_date, end_time) - datetime.combine(booking_date, start_time)
        minutes = delta.total_seconds() / 60
        if minutes not in (30, 60):
            messagebox.showerror("Error", "Bookings must be 30 minutes or 1 hour long.")
            return

        try:
            guests = int(guests_str)
            if guests <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Number of guests must be a positive integer.")
            return

        # Find or create a matching TimeSlot
        timeslot = None
        for ts in self.system.timeslots:
            if (ts.date == booking_date and
                ts.start_time == start_time and
                ts.end_time == end_time):
                timeslot = ts
                break

        if timeslot is None:
            timeslot = TimeSlot(
                timeslot_id=self.system.generateTimeSlotID(),
                date=booking_date,
                start_time=start_time,
                end_time=end_time,
                max_capacity=8,  #8 people per slot
                is_available=True,
            )
            self.system.timeslots.append(timeslot)

        try:
            booking = self.system.createBooking(customer, timeslot, guests)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        # Persist to CSV + update availability
        self.system.saveData()
        messagebox.showinfo("Success", f"Booking {booking.booking_id} created.")

        self.showCustomerHub(customer)


    # ------------  Staff Booking management page (same for higher and lower admins) ------------

    def showStaffCreateBookingPage(self,staff:Staff):
        self.show_frame(self.staffAdminBookingPage, staff)

    def staffAdminBookingPage(self, frame: tk.Frame, staff): # <-- booking page will be the same for staff and higher admins
        tk.Label(
            frame,
            text="Create Booking for Customer",
            font=("Helvetica", 20, "bold"),
            bg="#ffffff",
        ).pack(pady=10)

        top = tk.Frame(frame, bg="#ffffff")
        top.pack(pady=5)

        tk.Label(
            top,
            text="Customer email or ID:",
            font=("Helvetica", 12),
            bg="#ffffff",
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.staff_booking_customer_entry = tk.Entry(top, width=30)
        self.staff_booking_customer_entry.grid(row=0, column=1, padx=5, pady=5)

        #Calendar 
        cal_frame = tk.Frame(frame, bg="#ffffff")
        cal_frame.pack(side="left", padx=20, pady=10)

        tk.Label(
            cal_frame,
            text="Select date:",
            font=("Helvetica", 12, "bold"),
            bg="#ffffff",
        ).pack(anchor="w")

        self.staff_booking_calendar = Calendar(
            cal_frame,
            selectmode="day",
            date_pattern="yyyy-mm-dd",
        )
        self.staff_booking_calendar.pack(pady=5)

        # Time and guest selection on the right
        right = tk.Frame(frame, bg="#ffffff")
        right.pack(side="left", padx=40, pady=10, fill="y")

        tk.Label(right, text="From:", font=("Helvetica", 12), bg="#ffffff")\
            .grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Label(right, text="To:", font=("Helvetica", 12), bg="#ffffff")\
            .grid(row=1, column=0, padx=5, pady=5, sticky="w")

        times = []
        for h in range(9, 16):
            for m in (0, 30):
                times.append(f"{h:02d}:{m:02d}")
        times.append("16:00") 


        self.staff_from_combo = ttk.Combobox(right, values=times, width=10, state="readonly")
        self.staff_from_combo.grid(row=0, column=1, padx=5, pady=5)

        self.staff_to_combo = ttk.Combobox(right, values=times, width=10, state="readonly")
        self.staff_to_combo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(
            right,
            text="Number of guests:",
            font=("Helvetica", 12),
            bg="#ffffff",
        ).grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.staff_guests_spin = tk.Spinbox(right, from_=1, to=10, width=5)
        self.staff_guests_spin.grid(row=2, column=1, padx=5, pady=5)

        # Create booking button
        tk.Button(
            right,
            text="Create booking",
            font=("Helvetica", 14, "bold"),
            command=lambda: self.handleStaffCreateBooking(staff),
        ).grid(row=3, column=0, columnspan=2, pady=20)

        # Back button
        tk.Button(
            frame,
            text="Back",
            font=("Helvetica", 12),
            command=lambda: self.showStaffHub(staff) if not staff.higher_admin
                    else self.show_frame(self.adminHub, staff),
        ).pack(side="bottom", anchor="w", padx=10, pady=10)

      
    # -----------  Customer view and manage bookings page (edit/cancel) -----------
           
    def showCustomerViewBookingPage(self, customer: Customer):
        self.show_frame(self.customerViewBookingPage, customer)

    def customerViewBookingPage(self, frame: tk.Frame, customer: Customer):
        tk.Label(
            frame,
            text="My bookings",
            font=("Helvetica", 20, "bold"),
            bg="#ffffff",
        ).pack(pady=10)

        customer_bookings = [
            b for b in self.system.bookings
            if b.customer_id == customer.customer_id
        ]
        
        # Frame for table and scrollbar
        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("date", "start", "end", "guests", "status")

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10,
        )

        tree.heading("date", text="Date")
        tree.heading("start", text="Start")
        tree.heading("end", text="End")
        tree.heading("guests", text="Guests")
        tree.heading("status", text="Status")

        tree.column("date", width=100, anchor="center")
        tree.column("start", width=70, anchor="center")
        tree.column("end", width=70, anchor="center")
        tree.column("guests", width=60, anchor="center")
        tree.column("status", width=100, anchor="center")

        # Vertical scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        timeslot_by_id = {ts.timeslot_id: ts for ts in self.system.timeslots}

        self.customer_bookings_tree = tree 

        # Insert rows
        for booking in customer_bookings:
            ts = timeslot_by_id.get(booking.timeslot_id)
            if ts is None:
                # Placeholders in case timeslot was deleted after booking was made - should not normally happen, but just in case
                date_str = "?"
                start_str = "?"
                end_str = "?"
            else:
                date_str = formatDate(ts.date)
                start_str = formatTime(ts.start_time)
                end_str = formatTime(ts.end_time)

            tree.insert(
                "",
                "end",
                iid=booking.booking_id,
                values=(
                    date_str,
                    start_str,
                    end_str,
                    booking.number_of_guests,
                    booking.status,
                ),
            )

        buttons_frame = tk.Frame(frame, bg="#ffffff")
        buttons_frame.pack(pady=10)

        tk.Button(
            buttons_frame,
            text="Edit selected",
            font=("Helvetica", 12),
            command=lambda: self.handleEditBooking(customer),
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            buttons_frame,
            text="Cancel selected",
            font=("Helvetica", 12),
            command=lambda: self.handleCancelBooking(customer),
        ).grid(row=0, column=1, padx=5)
        
        # Back button
        tk.Button(
            frame,
            text="Back",
            font=("Helvetica", 12),
            command=lambda: self.showCustomerHub(customer),
        ).pack(side="bottom", anchor="w", padx=10, pady=10)

    def _get_selected_booking(self) -> Optional[Booking]:
        tree = self.customer_bookings_tree
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a booking first.")
            return None

        booking_id = selected[0] 
        booking = next((b for b in self.system.bookings if b.booking_id == booking_id), None)
        if booking is None:
            messagebox.showerror("Error", "Selected booking not found.")
        return booking

    def handleCancelBooking(self, customer: Customer):
        booking = self._get_selected_booking()
        if booking is None:
            return

        if booking.status != "BOOKED":
            messagebox.showerror("Error", "Only bookings with status BOOKED can be cancelled.")
            return

        confirm = messagebox.askyesno(
            "Confirm cancel",
            f"Cancel booking {booking.booking_id}?"
        )
        if not confirm:
            return
        # Update booking and timeslot availability
        self.system.cancelBooking(booking)
        self.system.saveData()

        messagebox.showinfo("Cancelled", f"Booking {booking.booking_id} has been cancelled.")

        # Refresh the view
        self.showCustomerViewBookingPage(customer)

    def handleEditBooking(self, user):
        booking = self._get_selected_booking()
        if booking is None:
            return

        if booking.status != "BOOKED":
            messagebox.showerror("Error", "Only bookings with status BOOKED can be edited.")
            return

        new_guests_str = simpledialog.askstring(
            "Edit booking",
            f"Enter new number of guests (current: {booking.number_of_guests}):"
        )
        if new_guests_str is None:
            return

        try:
            new_guests = int(new_guests_str)
            if new_guests <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a positive integer.")
            return

        ts = next((t for t in self.system.timeslots if t.timeslot_id == booking.timeslot_id), None)
        if ts is None:
            messagebox.showerror("Error", "Time slot for this booking no longer exists.")
            return

        current_without_this = sum(
            b.number_of_guests
            for b in self.system.bookings
            if b.timeslot_id == ts.timeslot_id and b.status == "BOOKED" and b.booking_id != booking.booking_id
        )

        if current_without_this + new_guests > ts.max_capacity:
            messagebox.showerror("Error", "Cannot update: this would exceed the time slot capacity.")
            return

        booking.number_of_guests = new_guests
        self.system.recalculateTimeSlotAvailability(ts)
        self.system.saveData()

        messagebox.showinfo("Updated", f"Booking {booking.booking_id} has been updated.")

        if isinstance(user, Customer):
            self.showCustomerViewBookingPage(user)
        else: 
            self.showStaffViewBookingspage(user)

    def handleStaffCreateBooking(self, staff: Staff):
        cust_str = self.staff_booking_customer_entry.get().strip()
        if not cust_str:
            messagebox.showerror("Error", "Please enter a customer email or ID.")
            return

        if cust_str.upper().startswith("C") and cust_str[1:].isdigit():
          
            customer = next((c for c in self.system.customers if c.customer_id == cust_str), None)
        else:
            customer = self.system.findCustomerByEmail(cust_str)

        if customer is None:
            messagebox.showerror("Error", "Customer not found. Check the email/ID.")
            return
        #Getting booking details from the form
        date_str = self.staff_booking_calendar.get_date()
        from_str = self.staff_from_combo.get()
        to_str = self.staff_to_combo.get()
        guests_str = self.staff_guests_spin.get()

        if not (date_str and from_str and to_str and guests_str):
            messagebox.showerror("Error", "Please select date, start time, end time and number of guests.")
            return

        try:
            booking_date = parseDate(date_str)
            start_time = parseTime(from_str)
            end_time = parseTime(to_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format.")
            return

        if end_time <= start_time:
            messagebox.showerror("Error", "End time must be after start time.")
            return

        delta = datetime.combine(booking_date, end_time) - datetime.combine(booking_date, start_time)
        minutes = delta.total_seconds() / 60
        if minutes not in (30, 60):
            messagebox.showerror("Error", "Bookings must be 30 minutes or 1 hour long.")
            return

        try:
            guests = int(guests_str)
            if guests <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Number of guests must be a positive integer.")
            return

        #Find or create timeslot
        timeslot = None
        for ts in self.system.timeslots:
            if ts.date == booking_date and ts.start_time == start_time and ts.end_time == end_time:
                timeslot = ts
                break

        if timeslot is None:
            timeslot = TimeSlot(
                timeslot_id=self.system.generateTimeSlotID(),
                date=booking_date,
                start_time=start_time,
                end_time=end_time,
                max_capacity=8,  
                is_available=True,
            )
            self.system.timeslots.append(timeslot)

        #Booking capacity logic
        try:
            booking = self.system.createBooking(customer, timeslot, guests)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.system.saveData()
        messagebox.showinfo(
            "Success",
            f"Booking {booking.booking_id} created for {customer.first_name} {customer.surname}."
        )

        # Optionally go back to hub
        if staff.higher_admin:
            self.show_frame(self.adminHub, staff)
        else:
            self.showStaffHub(staff)

    # ----------- Staff view customers page and helper funcitions (for lower admins) ------------
   
    def showViewCustomersPage(self, staff: Staff):
        self.show_frame(self.staffViewCustomersPage, staff)

    def staffViewCustomersPage(self, frame: tk.Frame, staff_user: Staff):
        tk.Label(
            frame,
            text="All customers",
            font=("Helvetica", 20, "bold"),
            bg="#ffffff",
        ).pack(pady=10)

        # Search bar
        search_frame = tk.Frame(frame, bg="#ffffff")
        search_frame.pack(pady=5)

        tk.Label(
            search_frame,
            text="Search (name, email, ID, phone):",
            font=("Helvetica", 10),
            bg="#ffffff",
        ).pack(side="left", padx=5)

        self.customer_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.customer_search_var, width=30)
        search_entry.pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="Search",
            command=self.filterCustomersTable,
            image=self.search_image,
            font=("Helvetica", 10),
        ).pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="Clear",
            command=self.clearCustomerSearch,
            font=("Helvetica", 10),
        ).pack(side="left", padx=5)

        # Table of customers
        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("id", "first", "surname", "email", "phone")

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15,
        )
        self.staff_customers_tree = tree 

        tree.heading("id", text="ID")
        tree.heading("first", text="First name")
        tree.heading("surname", text="Surname")
        tree.heading("email", text="Email")
        tree.heading("phone", text="Phone")

        for col in columns:
            tree.column(col, width=120, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Initial fill
        self.populateCustomersTree()

        tk.Button(
            frame,
            text="Back",
            font=("Helvetica", 12),
            command=lambda: self.showStaffHub(staff_user),
        ).pack(side="bottom", anchor="w", padx=10, pady=10)

    def populateCustomersTree(self, filter_text: str = ""):
            tree = self.staff_customers_tree
            for iid in tree.get_children():                tree.delete(iid)
            ft = filter_text.lower().strip()
            for c in self.system.customers:
               values = (
                   c.customer_id,
                   c.first_name,
                   c.surname,
                   c.email,
                   c.phone_number,
               )
               if ft:
                   haystack = " ".join(str(v) for v in values).lower()
                   if ft not in haystack:
                       continue
               tree.insert("", "end", iid=c.customer_id, values=values)



    def filterCustomersTable(self):
        text = self.customer_search_var.get().strip()
        tree = self.staff_customers_tree

        for iid in tree.get_children():
            tree.delete(iid)

        if not text:
            self.populateCustomersTree("")
            return

        # Exact email match using binary search
        customer = self.system.findCustomerByEmail(text)
        if customer is not None:
            tree.insert(
                "",
                "end",
                iid=customer.customer_id,
                values=(
                    customer.customer_id,
                    customer.first_name,
                    customer.surname,
                    customer.email,
                    customer.phone_number,
                ),
            )
            return

        # Fall back to broad substring search if there is no exact email match
        ft = text.lower()
        for c in self.system.customers:
            values = (
                c.customer_id,
                c.first_name,
                c.surname,
                c.email,
                c.phone_number,
            )
            haystack = " ".join(str(v) for v in values).lower()
            if ft in haystack:
                tree.insert("", "end", iid=c.customer_id, values=values)


    def clearCustomerSearch(self):
        self.customer_search_var.set("")
        self.populateCustomersTree("")

    # ------------  Staff view all bookings page (for both higher and lower admins) ------------

    def showStaffViewBookingspage(self, staff: Staff):
        self.show_frame(self.staffViewAllBookingsPage, staff)
       
    def staffViewAllBookingsPage(self, frame: tk.Frame, staff_user: Staff):

        tk.Label(
            frame,
            text="All customer bookings",
            font=("Helvetica", 20, "bold"),
            bg="#ffffff",
        ).pack(pady=10)

        search_frame = tk.Frame(frame, bg="#ffffff")
        search_frame.pack(pady=5)

        tk.Label(
            search_frame,
            text="Search (customer or date YYYY-MM-DD):",
            font=("Helvetica", 10), 
            bg= "#ffffff",
        ).pack(side="left", padx=5)

        self.bookings_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.bookings_search_var, width=30)
        search_entry.pack(side="left", padx=5)  

        tk.Button(
            search_frame,
            text="Search",  
            image=self.search_image,    
            command=self.filterBookingsTable,
        ).pack(side="left", padx=5) 

        tk.Button(
            search_frame,
            text="Clear",
            font=("Helvetica", 10),
            command=self.clearBookingsSearch,
        ).pack(side="left", padx=5)


        customer_bookings = [
            b for b in self.system.bookings
        ]

        columns = ("customer","date", "start", "end", "guests", "status")

        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10,
        )

        tree.heading("customer", text="Customer")
        tree.heading("date", text="Date")
        tree.heading("start", text="Start")
        tree.heading("end", text="End")
        tree.heading("guests", text="Guests")
        tree.heading("status", text="Status")

        tree.column("customer", width=150, anchor="center")
        tree.column("date", width=100, anchor="center")
        tree.column("start", width=70, anchor="center")
        tree.column("end", width=70, anchor="center")
        tree.column("guests", width=60, anchor="center")
        tree.column("status", width=100, anchor="center")

        # Implementing vertical scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        timeslot_by_id = {ts.timeslot_id: ts for ts in self.system.timeslots}

        self.customer_bookings_tree = tree  

        self.populateBookingsTree("")

        buttons_frame = tk.Frame(frame, bg="#ffffff")
        buttons_frame.pack(pady=10)

        tk.Button(
            buttons_frame,
            text="Edit selected",
            font=("Helvetica", 12),
            command=lambda: self.handleEditBooking(staff_user),
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            buttons_frame,
            text="Cancel selected",
            font=("Helvetica", 12),
            command=lambda: self.handleCancelBooking(staff_user),
        ).grid(row=0, column=1, padx=5)


        tk.Button(
            frame,
            text="Back",
            font=("Helvetica", 12),
            command=(
                (lambda: self.showStaffHub(staff_user))
                if not staff_user.higher_admin
                else (lambda: self.show_frame(self.adminHub, staff_user))
            ),
        ).pack(side="bottom", anchor="w", padx=10, pady=10)


    def populateBookingsTree(self, filter_text: str = ""):
        tree = self.customer_bookings_tree

        # Clears the current rows 
        for iid in tree.get_children():
            tree.delete(iid)

        ft = filter_text.lower().strip()
        timeslot_by_id = {ts.timeslot_id: ts for ts in self.system.timeslots}

        for booking in self.system.bookings:
            ts = timeslot_by_id.get(booking.timeslot_id)

            if ts is None:
                date_str = "?"
                start_str = "?"
                end_str = "?"
                customer_str = "Unknown"
            else:
                customer_obj = next(
                    (c for c in self.system.customers if c.customer_id == booking.customer_id),
                    None,
                )
                customer_str = (
                    f"{customer_obj.first_name} {customer_obj.surname}"
                    if customer_obj
                    else "Unknown"
                )
                date_str = formatDate(ts.date)
                start_str = formatTime(ts.start_time)
                end_str = formatTime(ts.end_time)

            values = (
                customer_str,
                date_str,
                start_str,
                end_str,
                booking.number_of_guests,
                booking.status,
            )

            if ft:
                # allow searching by customer name, date, etc.
                haystack = " ".join(str(v) for v in values).lower()
                if ft not in haystack:
                    continue

            tree.insert(
                "",
                "end",
                iid=booking.booking_id,
                values=values,
            )


    def filterBookingsTable(self):
        text = self.bookings_search_var.get().strip()
        self.populateBookingsTree(text)

    def clearBookingsSearch(self):
        self.bookings_search_var.set("")
        self.populateBookingsTree("")

       

   # ----- Account management page for both customers and staff (editing details, changing password, etc.)

    def manageAccountPage(self, user):
    #  Passes through user to ensure the same page can be used for both customers and staff
        self.show_frame(self.buildManageAccountPage, user)


    def buildManageAccountPage(self, frame: tk.Frame, user):
        is_staff = isinstance(user, Staff)

        tk.Label(
            frame,
            text="Manage my account",
            font=("Helvetica", 20, "bold"),
            bg="#ffffff",
        ).pack(pady=20)

        form = tk.Frame(frame, bg="#ffffff")
        form.pack(pady=10)

        tk.Label(form, text="First name:", font=("Helvetica", 12), bg="#ffffff")\
            .grid(row=0, column=0, sticky="w", padx=5, pady=5)
        first_entry = tk.Entry(form, width=30)
        first_entry.grid(row=0, column=1, padx=5, pady=5)
        first_entry.insert(0, user.first_name)

        tk.Label(form, text="Surname:", font=("Helvetica", 12), bg="#ffffff")\
            .grid(row=1, column=0, sticky="w", padx=5, pady=5)
        surname_entry = tk.Entry(form, width=30)
        surname_entry.grid(row=1, column=1, padx=5, pady=5)
        surname_entry.insert(0, user.surname)

        tk.Label(form, text="Email:", font=("Helvetica", 12), bg="#ffffff")\
            .grid(row=2, column=0, sticky="w", padx=5, pady=5)
        email_entry = tk.Entry(form, width=30)
        email_entry.grid(row=2, column=1, padx=5, pady=5)
        email_entry.insert(0, user.email)

        tk.Label(form, text="Phone number:", font=("Helvetica", 12), bg="#ffffff")\
            .grid(row=3, column=0, sticky="w", padx=5, pady=5)
        phone_entry = tk.Entry(form, width=30)
        phone_entry.grid(row=3, column=1, padx=5, pady=5)
        phone_entry.insert(0, user.phone_number)

        tk.Label(form, text="New password:", font=("Helvetica", 12), bg="#ffffff")\
            .grid(row=4, column=0, sticky="w", padx=5, pady=5)
        new_pass_entry = tk.Entry(form, width=30, show="*")
        new_pass_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(form, text="Repeat new password:", font=("Helvetica", 12), bg="#ffffff")\
            .grid(row=5, column=0, sticky="w", padx=5, pady=5)
        repeat_pass_entry = tk.Entry(form, width=30, show="*")
        repeat_pass_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(form, text="Date of Birth (YYYY-MM-DD):", font=("Helvetica", 12), bg="#ffffff")\
            .grid(row=6, column=0, sticky="w", padx=5, pady=5)
        dob_entry = tk.Entry(form, width=30)
        dob_entry.grid(row=6, column=1, padx=5, pady=5)
        dob_entry.insert(0, formatDate(user.date_of_birth))

        

        def save_changes():
            fn = first_entry.get().strip()
            sn = surname_entry.get().strip()
            em = email_entry.get().strip()
            ph = phone_entry.get().strip()
            new_pw = new_pass_entry.get()
            dob_str = dob_entry.get().strip()
            rep_pw = repeat_pass_entry.get()

            if not (fn and sn and em and ph and dob_str):
                messagebox.showerror("Error", "Name, email, phone and DOB cannot be empty.")
                return

            try:
                new_dob = parseDate(dob_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
                return

            today = date.today()
            age = today.year - new_dob.year - ((today.month, today.day) < (new_dob.month, new_dob.day))
            if age < 16:
                messagebox.showerror("Error", "You must be at least 16 years old.")
                return

            if new_pw or rep_pw:
                if new_pw != rep_pw:
                    messagebox.showerror("Error", "New passwords do not match.")
                    return
                # Updates password if a new one was entered
                user.setPassword(new_pw)

            # Updates new fields
            user.editFirstName(fn)
            user.editSurname(sn)
            user.editEmail(em)
            user.editPhoneNumber(ph)
            user.editDateOfBirth(new_dob)
            
            self.system.saveData()

            messagebox.showinfo("Saved", "Your account details have been updated.")

            # Goes back to the correct hub depending on the type of user
            if isinstance(user, Customer):
                self.showCustomerHub(user)
            else:
                if isinstance(user, Staff) and user.higher_admin:
                    self.show_frame(self.adminHub, user)
                else:
                    self.showStaffHub(user)

        tk.Button(
            frame,
            text="Save changes",
            font=("Helvetica", 14, "bold"),
            command=save_changes,
        ).pack(pady=10)

        tk.Button(
            frame,
            text="Back",
            font=("Helvetica", 12),
            command=(
                (lambda: self.showCustomerHub(user))
                if isinstance(user, Customer)
                else (
                    (lambda: self.showStaffHub(user))
                    if not user.higher_admin
                    else (lambda: self.show_frame(self.adminHub, user))
                )
            ),
        ).pack(side="bottom", anchor="w", padx=10, pady=10)

        tk.Button(
            frame,
            text="Log out",
            font=("Helvetica", 12),
            command=self.logout,
        ).pack(pady=5)

        tk.Button(
            frame,
            text="Delete my account",
            font=("Helvetica", 12),
            fg="red",
            command=lambda: self.deleteAccount(user),
        ).pack(pady=10)

# ----------- Log out function, used by both staff and customers (just goes back to main menu) -------

    def logout(self):
        # Confirmation to logout 
        answer = messagebox.askyesno(
            "Log out",
            "Are you sure you want to log out?"
        )
        if not answer:
            return

        self.showMainMenu()

# ------- Delete account function, used by both staff and customers -------

    def deleteAccount(self, user):
        # Asks the user for confirmation before deleting their account. If they confirm, deletes the account and all associated data, then returns to the main menu.
        answer = messagebox.askyesno(
            "Confirm delete",
            "Are you sure you want to delete your account? This action cannot be undone."
        )
        if not answer:
            return  

        # Removes from the correct list on SystemManager
        if isinstance(user, Customer):
            self.system.customers = [c for c in self.system.customers if c.customer_id != user.customer_id]
        elif isinstance(user, Staff):
            self.system.staff = [s for s in self.system.staff if s.staff_id != user.staff_id]

        self.system.saveData()

        messagebox.showinfo("Account deleted", "Your account has been deleted.")

        self.showMainMenu()


# ----------- Admin hub (for higher admins) -----------

    def adminHub(self, frame: tk.Frame, admin: Staff):
        
        top_right = tk.Frame(frame, bg="#ffffff")
        top_right.pack(side="top", anchor="ne", padx=5, pady=5)
       
        
        tk.Label(
            top_right,
            text="MY ACCOUNT",
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
        ).pack(side="left", padx=(0, 8))

        account_button = tk.Button(
            top_right,
            text="Manage my account",
            image=self.account_image,
            font=("Helvetica", 14),
            command=lambda: self.manageAccountPage(admin),
        )
        account_button.pack(side="left")
       
        
        
        tk.Label(
            frame,
            text=f"Admin hub – welcome, {admin.first_name}",
            font=("Helvetica", 16, "bold"),
            bg="#ffffff",
        ).pack(pady=10)
         
       

        tk.Button(
            frame,
            text="Create a booking for a customer",
            font=("Helvetica", 14),
            command=lambda: self.showStaffCreateBookingPage(admin),
        ).pack(pady=5)

        tk.Button(
            frame,
            text="View all bookings",
            font=("Helvetica", 14),
            command=lambda a=admin: self.showStaffViewBookingspage(admin)
        ).pack(pady=5)

        tk.Button(
            frame,
            text="View all accounts",
            font=("Helvetica", 14),
            command=lambda a=admin: self.showViewAllAccounts(frame, a)    
        ).pack(pady=5)

        tk.Button(
            frame,
            text="Create Staff Account",
            font=("Helvetica", 14),
            command=lambda: self.showStaffAccountCreationPage(admin)
        ).pack(pady=5)

        tk.Button(
            frame,
            text="Manage time slots",
            font=("Helvetica", 14),
            command=lambda: self.showManageTimeSlotsPage(admin)
        ).pack(pady=5)

        self.addExitButton(frame)

# ----------- Admin create staff account page (only accessible by higher admins) -----------


    def showStaffAccountCreationPage(self, admin):
        self.show_frame(self.staffAccountCreationPage, admin)
   
    def staffAccountCreationPage(self, frame, admin):
        tk.Label(
            frame,
            text="Create Staff Account",
            font=("Helvetica", 20, "bold"),
            bg="#ffffff"
        ).pack(pady=20)

        form = tk.Frame(frame, bg="#ffffff")
        form.pack(pady=20)

        tk.Label(form, text="First Name", font=("Helvetica", 12), bg="#ffffff").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        firstnameentry = tk.Entry(form, width=30)
        firstnameentry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Surname", font=("Helvetica", 12), bg="#ffffff").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        surnameentry = tk.Entry(form, width=30)
        surnameentry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Email", font=("Helvetica", 12), bg="#ffffff").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        emailentry = tk.Entry(form, width=30)
        emailentry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form, text="Password", font=("Helvetica", 12), bg="#ffffff").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        passwordentry = tk.Entry(form, width=30, show="*")
        passwordentry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(form, text="Repeat Password", font=("Helvetica", 12), bg="#ffffff").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        repeatpasswordentry = tk.Entry(form, width=30, show="*")
        repeatpasswordentry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(form, text="Date of Birth YYYY-MM-DD", font=("Helvetica", 12), bg="#ffffff").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        dobentry = tk.Entry(form, width=30)
        dobentry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(form, text="Phone Number", font=("Helvetica", 12), bg="#ffffff").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        phoneentry = tk.Entry(form, width=30)
        phoneentry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(form, text="Higher Admin?", font=("Helvetica", 12), bg="#ffffff").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        higheradminvar = tk.BooleanVar(value=False)
        tk.Checkbutton(form, variable=higheradminvar, bg="#ffffff").grid(row=7, column=1, sticky="w", padx=5, pady=5)

        def submit():
            firstname = firstnameentry.get().strip()
            surname = surnameentry.get().strip()
            email = emailentry.get().strip()
            password = passwordentry.get().strip()
            repeatpassword = repeatpasswordentry.get().strip()
            dobstr = dobentry.get().strip()
            phone = phoneentry.get().strip()
            higheradmin = higheradminvar.get()

            if not firstname or not surname or not email or not password or not repeatpassword or not dobstr or not phone:
                messagebox.showerror("Staff sign up error", "All fields are required.")
                return

            if password != repeatpassword:
                messagebox.showerror("Staff sign up error", "Passwords do not match.")
                return

            try:
                dob = parseDate(dobstr)
            except ValueError:
                messagebox.showerror("Staff sign up error", "Invalid date format. Please use YYYY-MM-DD.")
                return

            try:
                self.system.registerStaff(firstname, surname, dob, email, phone, password, higheradmin)
                self.system.saveData()
                messagebox.showinfo("Success", "Staff account created successfully.")
                self.show_frame(self.adminHub, admin)
            except ValueError as e:
                messagebox.showerror("Staff sign up error", str(e))

        tk.Button(
            frame,
            text="Create Account",
            font=("Helvetica", 14, "bold"),
            command=submit
        ).pack(pady=10)

        tk.Button(
            frame,
            text="Back",
            font=("Helvetica", 12),
            command=lambda: self.show_frame(self.adminHub, admin)
        ).pack(side="bottom", anchor="w", padx=10, pady=10)

# ------------- Admin View all accounts page and helper functions (list of all customers and staff, with search) ------------

    def showViewAllAccounts(self, frame: tk.Frame, admin_user: Staff):
        self.show_frame(self.viewAllAccounts, admin_user)
        

    def viewAllAccounts(self, frame: tk.Frame, admin_user: Staff):
        tk.Label(
            frame,
            text="All accounts",
            font=("Helvetica", 20, "bold"),
            bg="#ffffff",
        ).pack(pady=10)

        search_frame = tk.Frame(frame, bg="#ffffff")
        search_frame.pack(pady=5)

        tk.Label(
            search_frame,
            text="Search (name, email, ID, phone):",
            font=("Helvetica", 10),
            bg="#ffffff",
        ).pack(side="left", padx=5)

        self.accounts_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.accounts_search_var, width=30)
        search_entry.pack(side="left", padx=5)

        tk.Button(
            search_frame
            , text="Search", 
            command=self.filterAccountsTable, 
            image=self.search_image, 
            font=("Helvetica", 10)
        ).pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="Clear",  
            command=self.clearAccountsSearch,
            font= ("Helvetica", 10),
            ).pack(side="left", padx=5)

        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("type", "id", "first", "surname", "email", "phone")

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=18,
        )

        self.accounts_tree = tree

        for col, text in zip(columns, ["Type", "ID", "First name", "Surname", "Email", "Phone"]):
            tree.heading(col, text=text)
            tree.column(col, width=110, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        
        self._populateAccountsTree()

        tk.Button(
            frame,
            text="Back",
            font=("Helvetica", 12),
            command=lambda: self.show_frame(self.adminHub, admin_user),
        ).pack(side="bottom", anchor="w", padx=10, pady=10)

    def _populateAccountsTree(self, filter_text: str = ""):
        tree = self.accounts_tree
        for iid in tree.get_children():
            tree.delete(iid)

        ft = filter_text.lower().strip()

        for c in self.system.customers:
            values = (
                "Customer",
                c.customer_id,
                c.first_name,
                c.surname,
                c.email,
                c.phone_number,
            )
            if ft:
                haystack = " ".join(str(v) for v in values).lower()
                if ft not in haystack:
                    continue
            tree.insert("", "end", iid=f"C-{c.customer_id}", values=values)

        for s in self.system.staff:
            role = "Admin" if s.higher_admin else "Staff"
            values = (
                role,
                s.staff_id,
                s.first_name,
                s.surname,
                s.email,
                s.phone_number,
            )
            if ft:
                haystack = " ".join(str(v) for v in values).lower()
                if ft not in haystack:
                    continue
            tree.insert("", "end", iid=f"S-{s.staff_id}", values=values)

    def filterAccountsTable(self):
        text = self.accounts_search_var.get().strip()
        tree = self.accounts_tree

        # Clears the current rows in the tree
        for iid in tree.get_children():
            tree.delete(iid)

        if not text:
            self._populateAccountsTree("")
            return

        # Exact email match shortcut (binary search on sorted emails)
        if "@" in text:
            customer = self.system.findCustomerByEmail(text)
            staff = self.system.findStaffByEmail(text)

            # Show customer match if it is found
            if customer is not None:
                tree.insert(
                    "",
                    "end",
                    iid=f"C-{customer.customer_id}",
                    values=(
                        "Customer",
                        customer.customer_id,
                        customer.first_name,
                        customer.surname,
                        customer.email,
                        customer.phone_number,
                    ),
                )

            if staff is not None:
                role = "Admin" if staff.higher_admin else "Staff"
                tree.insert(
                    "",
                    "end",
                    iid=f"S-{staff.staff_id}",
                    values=(
                        role,
                        staff.staff_id,
                        staff.first_name,
                        staff.surname,
                        staff.email,
                        staff.phone_number,
                    ),
                )

            # if found at least one exact email, it will stop here and not do the broad search
            if customer is not None or staff is not None:
                return
            

        # Generic substring search across all customer and staff fields
        ft = text.lower()

        for c in self.system.customers:
            values = (
                "Customer",
                c.customer_id,
                c.first_name,
                c.surname,
                c.email,
                c.phone_number,
            )
            haystack = " ".join(str(v) for v in values).lower()
            if ft in haystack:
                tree.insert("", "end", iid=f"C-{c.customer_id}", values=values)

        for s in self.system.staff:
            role = "Admin" if s.higher_admin else "Staff"
            values = (
                role,
                s.staff_id,
                s.first_name,
                s.surname,
                s.email,
                s.phone_number,
            )
            haystack = " ".join(str(v) for v in values).lower()
            if ft in haystack:
                tree.insert("", "end", iid=f"S-{s.staff_id}", values=values)


    def clearAccountsSearch(self):
        self.accounts_search_var.set("")
        self._populateAccountsTree("")


# ------------ Admin time slot management page (toggling availability, setting max capacity, etc.) ------------

    def showManageTimeSlotsPage(self, admin: Staff):
        self.show_frame(self.manageTimeSlots, admin)
   
    def manageTimeSlots(self, frame:tk.Frame, admin: Staff): 
       
        tk.Label(
            frame,
            text="Manage time slots",
            font=("Helvetica", 20, "bold"),
            bg="#ffffff",
         ).pack(pady=10)

        main = tk.Frame(frame, bg="#ffffff")
        main.pack(padx=20, pady=10, fill="both", expand=True)

        # Calendar for selecting date, displayed on the left of the screen
        cal_frame = tk.Frame(main, bg="#ffffff")
        cal_frame.pack(side="left", padx=20, pady=10)

        tk.Label(
            cal_frame,
            text="Select date",
            font=("Helvetica", 12, "bold"),
            bg="#ffffff",
        ).pack(anchor="w")

        self.timeslot_calendar = Calendar(
            cal_frame,
            selectmode="day",
            date_pattern="yyyy-mm-dd", 
        )
        self.timeslot_calendar.pack(pady=5)

        
        right = tk.Frame(main, bg="#ffffff")
        right.pack(side="left", padx=40, pady=10, fill="y")

        tk.Label(right, text="From", font=("Helvetica", 12), bg="#ffffff").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        tk.Label(right, text="To", font=("Helvetica", 12), bg="#ffffff").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )

        times = []
        for h in range(9, 16): 
            for m in (0, 30):
                times.append(f"{h:02d}:{m:02d}")
        times.append("16:00")   

        self.manage_from_combo = ttk.Combobox(
            right, values=times, width=10, state="readonly"
        )
        self.manage_from_combo.grid(row=0, column=1, padx=5, pady=5)

        self.manage_to_combo = ttk.Combobox(
            right, values=times, width=10, state="readonly"
        )
        self.manage_to_combo.grid(row=1, column=1, padx=5, pady=5)

        # label to show current status of the selected slot
        self.timeslot_status_label = tk.Label(
            right,
            text="Select date and times, then click 'Toggle'.",
            font=("Helvetica", 10),
            bg="#ffffff",
        )
        self.timeslot_status_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        tk.Button(
            right,
            text="Toggle availability",
            font=("Helvetica", 14, "bold"),
            command=self.handleToggleAdminTimeSlot,
        ).grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(
            frame,
            text="Back",
            font=("Helvetica", 12),
            command=lambda: self.show_frame(self.adminHub, admin),
         ).pack(side="bottom", anchor="w", padx=10, pady=10)

    def handleToggleAdminTimeSlot(self):
        date_str = self.timeslot_calendar.get_date()
        from_str = self.manage_from_combo.get()
        to_str = self.manage_to_combo.get()

        if not (date_str and from_str and to_str):
            messagebox.showerror("Error", "Please select date, start time and end time.")
            return

        try:
            slot_date = parseDate(date_str)
            start_time = parseTime(from_str)
            end_time = parseTime(to_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format.")
            return

        if end_time <= start_time:
            messagebox.showerror("Error", "End time must be after start time.")
            return

        # 30-60 minute slots logic 
        delta = datetime.combine(slot_date, end_time) - datetime.combine(slot_date, start_time)
        minutes = delta.total_seconds() / 60
        if minutes not in (30, 60):
            messagebox.showerror("Error", "Time slots must be 30 minutes or 1 hour long.")
            return

        # Find existing timeslot
        ts = None
        for t in self.system.timeslots:
            if t.date == slot_date and t.start_time == start_time and t.end_time == end_time:
                ts = t
                break

        if ts is None:
            # Create a new timeslot, set to available
            ts = TimeSlot(
                timeslot_id=self.system.generateTimeSlotID(),
                date=slot_date,
                start_time=start_time,
                end_time=end_time,
                max_capacity=8,  
                is_available=True,
            )
            self.system.timeslots.append(ts)
        
        ts.is_available = not ts.is_available # This toggles availability, allowing admins to both disable and enable time slots as needed
        self.system._save_timeslots()

        status_text = "available" if ts.is_available else "unavailable"
        self.timeslot_status_label.config(
            text=f"Time slot {formatDate(ts.date)} {formatTime(ts.start_time)}–{formatTime(ts.end_time)} is now {status_text}."
        )
        messagebox.showinfo("Updated", f"Time slot is now {status_text}.")



#---- MAIN Application here -------

if __name__ == "__main__":
    system_manager = SystemManager()
    root = tk.Tk()
    app = MeowMochaApp(root, system_manager)
    root.mainloop() 

        
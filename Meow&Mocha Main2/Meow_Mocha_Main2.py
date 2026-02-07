from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
import csv
import pickle
import os
import tkinter as tk
from tkinter import Frame, messagebox, Image, PhotoImage
from typing import Optional

#-- password hashing, date time conversions here (helper functions)

def hashPassword(plain:str) -> str:
    return plain[::-1]  #placeholder (not plain text)

def verifyPassword(plain:str, hashed:str) -> bool:
    return hashPassword(plain) == hashed

#date time conversions here
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

#--data classes

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

#---- system manager with methods properly defined inside the class ----

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

    # load / save API
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

    # lookups and searches (binary search expects sorted lists)
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

    # registering and logging in users here -come back to this to add validation checks 
    def registerCustomer(self, first_name: str, surname: str, date_of_birth: date, email: str, phone_number: str, plain_password: str) -> Customer:
        customer_id = self.generateCustomerID()
        password_hash = hashPassword(plain_password)
        new_customer = Customer(
            customer_id=customer_id,
            first_name=first_name,
            surname=surname,
            date_of_birth=date_of_birth,
            email=email,
            phone_number=phone_number,
            password_hash=password_hash
        )
        self.customers.append(new_customer)
        self.customers.sort(key=lambda c: c.email)  # keep sorted by email so that binary search works
        return new_customer

    def loginCustomer(self, email: str, plain_password: str) -> Optional[Customer]:
        found = self.findCustomerByEmail(email)
        if found and verifyPassword(plain_password, found.password_hash):
            return found
        return None

    def registerStaff(self, first_name: str, surname: str, date_of_birth: date, email: str, phone_number: str, plain_password: str, higher_admin: bool) -> Staff:
        staff_id = self.generateStaffID()
        password_hash = hashPassword(plain_password)
        new_staff = Staff(
            staff_id=staff_id,
            first_name=first_name,
            surname=surname,
            date_of_birth=date_of_birth,
            email=email,
            phone_number=phone_number,
            password_hash=password_hash,
            higher_admin=higher_admin
        )
        self.staff.append(new_staff)
        self.staff.sort(key=lambda s: s.email)  # keep sorted by email for the binary search 
        return new_staff

    def loginStaff(self, email: str, plain_password: str) -> Optional[Staff]:
        found = self.findStaffByEmail(email)
        if found and verifyPassword(plain_password, found.password_hash):
            return found
        return None

    # Time slot and capacity management
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

    # Booking management
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
        # update timeslot availability
        timeslot = next((ts for ts in self.timeslots if ts.timeslot_id == booking.timeslot_id), None)
        if timeslot:
            self.recalculateTimeSlotAvailability(timeslot)

# -- GUI classes and functions here (login screen, main menu, etc.)

class MeowMochaApp:
    def __init__(self, root: tk.Tk, system: SystemManager):
        self.root = root
        self.system = system
        self.root.configure(bg = "#ffc4df"  ) #pink background 
        self.root.title("Meow&Mocha System")
        self.root.minsize(800, 500)  

        self.logo_image = tk.PhotoImage(file="MM3.png")
        # load data from the system manager (method exists on SystemManager)
        self.system.loadData()
        self.current_frame = None
        self.showMainMenu()

    def show_frame (self, builder_function, *args):
        if self.current_frame is not None:
            self.current_frame.destroy()
        
        frame = tk.Frame(self.root, bg ="#FFFFFF")
        frame.pack(padx=20, pady=20,fill="both", expand=True )
        self.current_frame = frame

        builder_function(frame, *args) #Call a "builder function" to populate the frame
   
       
    def showMainMenu(self):
        self.show_frame(self.build_main_menu)


    def build_main_menu(self, frame: tk.Frame):
        #logo label 
        logo_label = tk.Label(frame, image=self.logo_image, bg = "#ffffff" )
        logo_label.pack(pady=10)
        
        tk.Label(
            frame,
            text = "Welcome to Meow&Mocha!",
            font = ("Helvetica", 16, "bold"),
            bg = "#ffffff",
        ).pack(pady=10)

        tk.Button(
            frame,
            text="Customer Portal",
            font = ("Helvetica", 12),
            width=20,
            command = self.showCustomerLogIn
        ).pack(pady=5)
        tk.Button(
            frame,
            text="Staff Portal",
            font = ("Helvetica", 12),
            width=20,
            command= self.showStaffLogIn
            #command will go here (show_staff_login)
            
        ).pack(pady=5)#
        tk.Button(
            frame,
            text="Admin Portal",
            font = ("Helvetica", 12),
            width=20,
            #command will go here (show_admin_login)
            
        ).pack(pady=5)

    # ──────  Customer Portals fpr LOG IN and SIGN UP here ───────────

    def showCustomerLogIn(self):
        self.show_frame(self.buildCustomerLogInPortal)

    def buildCustomerLogInPortal(self, frame: tk.Frame): #Might change this - may add these as functions inside building main menu, destrpy label to switch page 
        tk.Label(
            frame,
            text="Customer Login",
            font=("Helvetica", 16, "bold"),
            bg="#ffffff",
        ).pack(pady=40)

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
            command=lambda: self.handle_customer_login(email_entry.get(),
                                                       password_entry.get()),
        ).pack(pady=10)

        tk.Label(
            frame,
            text="Not a Customer yet?",
            font=("Helvetica", 10),
            bg="#ffffff",
        ).pack(pady=20)

        tk.Button(
            frame,
            text="Sign up",
            font=("Helvetica", 10, "bold"),
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

        self.show_frame(self.buildCustomerHub, customer)
        self.showCustomerHub(customer)



    def showCustomerSignUp(self):

        self.show_frame(self.buildCustomerSignUpPortal)

    def buildCustomerSignUpPortal(self, frame: tk.Frame):
        tk.Label(
            frame,
            text="Customer Sign up",
            font=("Helvetica", 16, "bold"),
            bg="#ffffff",
        ).pack(pady=35)

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

        password_entry = tk.Entry(form, width=30)
        password_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(
            form,
            text="Repeat password:",
            font=("Helvetica", 12),
            bg="#ffffff",
        ).grid(row=4, column=0, sticky="w", padx=5, pady=5)

        repeatpassword_entry = tk.Entry(form, width=30)
        repeatpassword_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(
            form,
            text="Date of Birth:",
            font=("Helvetica", 12),
            bg="#ffffff",
        ).grid(row=5, column=0, sticky="w", padx=5, pady=5)

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
                phone_entry.get()
                #Date of birth entry to be added later 
                ),
        ).pack(pady=10)

        tk.Button(
            frame,
            text="Back",
            command=self.showCustomerLogIn,
            font = ("Helvetica", 12),
        ).pack (side= "bottom" , anchor="w",padx= 10, pady=10)

    #Staff Portals for LOG IN here

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
            command=lambda: self.handle_staff_login(email_entry.get(),
                                                       password_entry.get()),
        ).pack(pady=10)

        tk.Button(
            frame,
            text="Back",
            command=self.showMainMenu,
            font = ("Helvetica", 12),
        ).pack (side= "bottom" , anchor="w",padx= 10, pady=10)

    def handleCustomerSignUp(self):
        pass

    def handle_staff_login(self, email: str, password: str):
        # later: call your SystemManager login here, then
        # self._show_frame(self.buildStaffHub, staff)
        pass

    #   ------------  Customer Hub here  ------------
    def showCustomerHub(self, customer: Customer):
        self.show_frame(self.buildCustomerHub, customer)

    def buildCustomerHub(self, frame:tk.Frame, customer: Customer):
        
        tk.Label(
            frame,
            text = "Welcome to Meow&Mocha!",
            font = ("Helvetica", 16, "bold"),
            bg = "#ffffff",
        ).pack(pady=10)

    #   ------------  Staff Hub here    ------------

    def buildStaffHub(self, staff: Staff):
        pass
    def customerBookingPage(self):
        pass
    def staffAdminBookingPage(self): # <-- booking page will be the same for staff and higher admins
        pass   

    def customerViewBookingPage(self, customer: Customer):
        pass
    def staffViewCustomersPage(self, staff: Staff):
        pass
    def staffViewAllBookingsPage(self, staff: Staff):
        pass
    def manageAccountPage(self, user):
        pass
    def adminHub(self, admin: Staff):
        pass
    def createStaffAccount(self, admin: Staff):
        pass
    def viewAllAccounts(self, admin: Staff):
        pass
    def manageTimeSlots(self, admin: Staff): #managing time slots, toggling avaiability
        pass



        









#---- MAIN Application loop here! --- temporary placeholder ----

if __name__ == "__main__":
    # Initialize system manager
    system_manager = SystemManager()
    # no separate init() required now because __init__ performs setup
    root = tk.Tk()

    app = MeowMochaApp(root, system_manager)
    root.mainloop() #wait for events 




    # ---TO DO LIST---
        # Add validation when registering customer and staff, refer to my pseudocode notes in design 
        # Complete all GUI pages and link them together
        # Check that the log ins work correctly
        # Create time slot management screen design for the documentation 
        # Add a calendar widget for selecting dates in the booking screen
        # On application exit, save data
        # Organise time slots so that you can select either 30 minute sessions or 1 hour sessions




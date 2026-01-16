from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
import csv
import pickle
import os
import tkinter as tk

#-- password hashing, date time conversions here (helper functions)

def hashPassword(plain:str) -> str:
    return plain [::-1]  #placeholder (not plain text)
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

        #set password method here
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



 #---- system functions (generating primary keys, creating lists) ----

class SystemManager:
    def init(self) -> None:
        self.customers: list[Customer] = []
        self.staff: list[Staff] = []
        self.timeslots: list[TimeSlot] = []
        self.bookings: list[Booking] = []

        self.next_customer_id: int = 1
        self.next_staff_id: int = 1
        self.next_timeslot_id: int = 1
        self.next_booking_id: int = 1

def generateCustomerID(self) -> str:
    cID = f"C{self.next_customer_id:05d}"
    self.next_customer_id += 1
    return cID

def generateStaffID(self) -> str:   
    sID = f"S{self.next_staff_id:05d}"
    self.next_staff_id += 1#
    return sID

def generateTimeSlotID(self) -> str:
    tID = f"T{self.next_timeslot_id:05d}"
    self.next_timeslot_id += 1
    return tID

def generateBookingID(self) -> str:
    bID = f"B{self.next_booking_id:05d}"
    self.next_booking_id += 1
    return bID
    

 #-----    file loading and saving functions here

def loadData(self) -> None:
    self._loadCustomers()
    self._loadStaff()
    self._loadTimeSlots()
    self._loadBookings()
    

def saveData(self) -> None:
    self._saveCustomers()  
    self._saveStaff()
    self._saveTimeSlots()
    self._saveBookings()

def _loadCustomers(self) -> None:
    if os.path.exists("customers.pkl"):
        with open("customers.pkl", "rb") as f:
            self.customers = pickle.load(f)
        #set next customer id
        if self.customers:
            max_id_num = max(int(c.customer_id[1:]) for c in self.customers)
            self.next_customer_id = max_id_num + 1

def _save_customers(self) -> None:
    with open("customers.pkl", "wb") as f:
        pickle.dump(self.customers, f)

def _loadStaff(self) -> None:
    if os.path.exists("staff.pkl"):
        with open("staff.pkl", "rb") as f:
            self.staff = pickle.load(f)
        #set next staff id
        if self.staff:
            max_id_num = max(int(s.staff_id[1:]) for s in self.staff)
            self.next_staff_id = max_id_num + 1

def _saveStaff(self) -> None:
    with open("staff.pkl", "wb") as f:
        pickle.dump(self.staff, f)
    


 #-----    lookups and searches here 





 #-----    Time slot and capacity management here -----




 #-- GUI classes and functions here (login screen, main menu, etc.)


 #---- MAIN Application loop here! --- temporary placeholder ----
if __name__ == "__main__":
    # Initialize system manager
    system_manager = SystemManager()
    system_manager.init()
    # Placeholder for GUI initialization
    root = tk.Tk()
    root.title("Meow&Mocha Booking System")

    # Placeholder for main application loop
    root.mainloop() #wait for events 
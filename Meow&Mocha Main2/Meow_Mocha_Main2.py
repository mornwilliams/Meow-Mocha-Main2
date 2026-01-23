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
                is_available=row["is_available"].lower() == "true"
            )
            self.timeslots.append(timeslot)
        #set next timeslot id
        if self.timeslots:
            max_id_num = max(int(t.timeslot_id[1:]) for t in self.timeslots)
            self.next_timeslot_id = max_id_num + 1

def _saveTimeSlots(self) -> None:
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
def _loadBookings(self) -> None:
    self.bookings = []
    if not os.path.exists("bookings.csv"):
        return
    with open("bookings.csv", "r", newline='', encoding="utf-8") as f:
        csv.reader = csv.DictReader(f)
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
            #set next booking id    
            if self.bookings:
                max_id_num = max(int(b.booking_id[1:]) for b in self.bookings)
                self.next_booking_id = max_id_num + 1

def _saveBookings(self) -> None:
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

    


 #-----    lookups and searches here - remeber to sort customers before implementing binary search -----





 #-----    Time slot and capacity management here -----

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

 #-----   Booking management here -----

# Creating a booking/ canceling booking 

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
    #update timeslot availability
    timeslot = next((ts for ts in self.timeslots if ts.timeslot_id == booking.timeslot_id), None)
    if timeslot:
        self.recalculateTimeSlotAvailability(timeslot)

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
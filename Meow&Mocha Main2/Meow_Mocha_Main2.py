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

    def editCustomerDetails():
        pass

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
    def editStaffDetails():
        pass

@dataclass
class TimeSlot:
    timeslot_id: str
    date: date
    start_time: time
    end_time: time
    max_capacity: int
    is_available: bool=True

    #duration method here
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
        pass
    #complete method here
    def completeBooking(self):
        pass

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
    

 # file loading and saving functions



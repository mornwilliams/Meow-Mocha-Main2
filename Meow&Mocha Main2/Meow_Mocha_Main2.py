from dataclasses import dataclass, field
from datetime import date, datetime, time
import csv
import pickle
import os

@dataclass
class Customer:
    customer_id: str
    first_name: str
    surname:str
    date_of_birth: date
    email:str
    phone_number:str
    password_hash:str

    #editing methods

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

@dataclass
class TimeSlot:
    timeslot_id: str
    date: date
    start_time: time
    end_time: time
    max_capacity: int
    is_available: bool=True

    #duration method here

@dataclass
class Booking:  
    booking_id: str
    customer_id: str
    timeslot_id: str
    number_of_guests: int
    status: str #such as "BOOKED", "CANCELLED", "COMPLETED"           
    booking_timestamp: datetime = field(default_factory=datetime.now)

    #cancel method here
    #complete method here

 #--system functions (generating primary keys, creating lists)
 # file loading and saving functions



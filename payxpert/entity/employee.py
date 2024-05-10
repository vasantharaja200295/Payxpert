# entity/employee.py
from datetime import date

class Employee:
    def __init__(self, employee_id=None, first_name=None, last_name=None, date_of_birth=None, gender=None,
                 email=None, phone_number=None, address=None, position=None, joining_date=None, termination_date=None):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.position = position
        self.joining_date = joining_date
        self.termination_date = termination_date

    def calculate_age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
            age -= 1
        return age


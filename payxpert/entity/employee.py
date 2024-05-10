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

# entity/payroll.py
class Payroll:
    def __init__(self, payroll_id=None, employee_id=None, pay_period_start_date=None, pay_period_end_date=None,
                 basic_salary=None, overtime_pay=None, deductions=None, net_salary=None):
        self.payroll_id = payroll_id
        self.employee_id = employee_id
        self.pay_period_start_date = pay_period_start_date
        self.pay_period_end_date = pay_period_end_date
        self.basic_salary = basic_salary
        self.overtime_pay = overtime_pay
        self.deductions = deductions
        self.net_salary = net_salary

# entity/tax.py
class Tax:
    def __init__(self, tax_id=None, employee_id=None, tax_year=None, taxable_income=None, tax_amount=None):
        self.tax_id = tax_id
        self.employee_id = employee_id
        self.tax_year = tax_year
        self.taxable_income = taxable_income
        self.tax_amount = tax_amount

# entity/financial_record.py
class FinancialRecord:
    def __init__(self, record_id=None, employee_id=None, record_date=None, description=None, amount=None, record_type=None):
        self.record_id = record_id
        self.employee_id = employee_id
        self.record_date = record_date
        self.description = description
        self.amount = amount
        self.record_type = record_type
from dao.employee_service import EmployeeService
from dao.payroll_service import PayrollService
from dao.tax_service import TaxService
from dao.financial_record_service import FinancialRecordService
from entity.employee import Employee
from util.db_conn_util import get_connection
from datetime import date
from exception.employee_not_found_exception import EmployeeNotFoundException
from exception.payroll_generation_exception import PayrollGenerationException
from exception.tax_calculation_exception import TaxCalculationException
from exception.financial_record_exception import FinancialRecordException

def main():

    db_connection = get_connection()

    employee_service = EmployeeService(db_connection)
    payroll_service = PayrollService(db_connection)
    tax_service = TaxService(db_connection)
    financial_record_service = FinancialRecordService(db_connection)

    while True:
        print("\nPayXpert Payroll Management System")
        print("1. Employee Management")
        print("2. Payroll Processing")
        print("3. Tax Calculation")
        print("4. Financial Record Management")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            employee_management(employee_service)
        elif choice == "2":
            payroll_processing(employee_service, payroll_service)
        elif choice == "3":
            tax_calculation(employee_service, tax_service)
        elif choice == "4":
            financial_record_management(employee_service, financial_record_service)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

    db_connection.close()

def employee_management(employee_service):
    while True:
        print("\nEmployee Management")
        print("1. Add Employee")
        print("2. Update Employee")
        print("3. Remove Employee")
        print("4. View Employee Details")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_employee(employee_service)
        elif choice == "2":
            update_employee(employee_service)
        elif choice == "3":
            remove_employee(employee_service)
        elif choice == "4":
            view_employee_details(employee_service)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def add_employee(employee_service):
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
    gender = input("Enter gender (M/F): ")
    email = input("Enter email: ")
    phone_number = input("Enter phone number: ")
    address = input("Enter address: ")
    position = input("Enter position: ")
    joining_date = input("Enter joining date (YYYY-MM-DD): ")

    employee = Employee(
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date.fromisoformat(date_of_birth),
        gender=gender,
        email=email,
        phone_number=phone_number,
        address=address,
        position=position,
        joining_date=date.fromisoformat(joining_date)
    )

    employee_service.add_employee(employee)
    print("Employee added successfully.")

def update_employee(employee_service):
    employee_id = int(input("Enter employee ID: "))

    try:
        employee = employee_service.get_employee_by_id(employee_id)
    except EmployeeNotFoundException as e:
        print(e)
        return

    first_name = input(f"Enter first name ({employee.first_name}): ") or employee.first_name
    last_name = input(f"Enter last name ({employee.last_name}): ") or employee.last_name
    date_of_birth = input(f"Enter date of birth ({employee.date_of_birth.isoformat()}): ") or employee.date_of_birth
    gender = input(f"Enter gender ({employee.gender}): ") or employee.gender
    email = input(f"Enter email ({employee.email}): ") or employee.email
    phone_number = input(f"Enter phone number ({employee.phone_number}): ") or employee.phone_number
    address = input(f"Enter address ({employee.address}): ") or employee.address
    position = input(f"Enter position ({employee.position}): ") or employee.position
    joining_date = input(f"Enter joining date ({employee.joining_date.isoformat()}): ") or employee.joining_date
    termination_date = input(f"Enter termination date ({employee.termination_date.isoformat() if employee.termination_date else None}): ") or employee.termination_date

    updated_employee = Employee(
        employee_id=employee_id,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date.fromisoformat(date_of_birth) if isinstance(date_of_birth, str) else date_of_birth,
        gender=gender,
        email=email,
        phone_number=phone_number,
        address=address,
        position=position,
        joining_date=date.fromisoformat(joining_date) if isinstance(joining_date, str) else joining_date,
        termination_date=date.fromisoformat(termination_date) if isinstance(termination_date, str) else termination_date
    )

    employee_service.update_employee(updated_employee)
    print("Employee updated successfully.")

def remove_employee(employee_service):
    employee_id = int(input("Enter employee ID: "))
    employee_service.remove_employee(employee_id)
    print("Employee removed successfully.")

def view_employee_details(employee_service):
    employee_id = int(input("Enter employee ID: "))

    try:
        employee = employee_service.get_employee_by_id(employee_id)
    except EmployeeNotFoundException as e:
        print(e)
        return

    print(f"\nEmployee Details:")
    print(f"Employee ID: {employee.employee_id}")
    print(f"First Name: {employee.first_name}")
    print(f"Last Name: {employee.last_name}")
    print(f"Date of Birth: {employee.date_of_birth.isoformat()}")
    print(f"Gender: {employee.gender}")
    print(f"Email: {employee.email}")
    print(f"Phone Number: {employee.phone_number}")
    print(f"Address: {employee.address}")
    print(f"Position: {employee.position}")
    print(f"Joining Date: {employee.joining_date.isoformat()}")
    print(f"Termination Date: {employee.termination_date.isoformat() if employee.termination_date else 'N/A'}")

def payroll_processing(employee_service, payroll_service):
    while True:
        print("\nPayroll Processing")
        print("1. Generate Payroll")
        print("2. View Payroll Details")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            generate_payroll(employee_service, payroll_service)
        elif choice == "2":
            view_payroll_details(employee_service, payroll_service)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def generate_payroll(employee_service, payroll_service):
    employee_id = int(input("Enter employee ID: "))
    try:
        employee = employee_service.get_employee_by_id(employee_id)
    except EmployeeNotFoundException as e:
        print(e)
        return

    start_date = input("Enter pay period start date (YYYY-MM-DD): ")
    end_date = input("Enter pay period end date (YYYY-MM-DD): ")

    try:
        payroll_service.generate_payroll(employee_id, date.fromisoformat(start_date), date.fromisoformat(end_date))
    except PayrollGenerationException as e:
        print(e)
        return

    print("Payroll generated successfully.")

def view_payroll_details(employee_service, payroll_service):
    employee_id = int(input("Enter employee ID: "))
    try:
        employee = employee_service.get_employee_by_id(employee_id)
    except EmployeeNotFoundException as e:
        print(e)
        return

    payrolls = payroll_service.get_payrolls_for_employee(employee_id)

    if not payrolls:
        print("No payroll records found for this employee.")
        return

    print(f"\nPayroll Records for Employee {employee.first_name} {employee.last_name}:")
    for payroll in payrolls:
        print(f"\nPayroll ID: {payroll.payroll_id}")
        print(f"Pay Period: {payroll.pay_period_start_date.isoformat()} - {payroll.pay_period_end_date.isoformat()}")
        print(f"Basic Salary: {payroll.basic_salary}")
        print(f"Overtime Pay: {payroll.overtime_pay}")
        print(f"Deductions: {payroll.deductions}")
        print(f"Net Salary: {payroll.net_salary}")
        
def tax_calculation(employee_service, tax_service):
    while True:
        print("\nTax Calculation")
        print("1. Calculate Tax")
        print("2. View Tax Details")
        print("3. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            calculate_tax(employee_service, tax_service)
        elif choice == "2":
            view_tax_details(employee_service, tax_service)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")
            
def calculate_tax(employee_service, tax_service):
    employee_id = int(input("Enter employee ID: "))
    tax_year = int(input("Enter tax year: "))
    try:
        employee = employee_service.get_employee_by_id(employee_id)
    except EmployeeNotFoundException as e:
        print(e)
        return

    try:
        tax_service.calculate_tax(employee_id, tax_year)
    except TaxCalculationException as e:
        print(e)
        return

    print("Tax calculated successfully.")
    
    
def view_tax_details(employee_service, tax_service):
    employee_id = int(input("Enter employee ID: ")) 
    try:
        employee = employee_service.get_employee_by_id(employee_id)
    except EmployeeNotFoundException as e:
        print(e)
        return

    taxes = tax_service.get_taxes_for_employee(employee_id)

    if not taxes:
        print("No tax records found for this employee.")
        return

    print(f"\nTax Records for Employee {employee.first_name} {employee.last_name}:")
    for tax in taxes:
        print(f"\nTax ID: {tax.tax_id}")
        print(f"Tax Year: {tax.tax_year}")
        print(f"Taxable Income: {tax.taxable_income}")
        print(f"Tax Amount: {tax.tax_amount}")
        
        
def financial_record_management(employee_service, financial_record_service):
    while True:
        print("\nFinancial Record Management")
        print("1. Add Financial Record")
        print("2. View Financial Records")
        print("3. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_financial_record(employee_service, financial_record_service)
        elif choice == "2":
            view_financial_records(employee_service, financial_record_service)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def add_financial_record(employee_service, financial_record_service):
    employee_id = int(input("Enter employee ID: "))
    try:
        employee = employee_service.get_employee_by_id(employee_id)
    except EmployeeNotFoundException as e:
        print(e)
        return

    description = input("Enter description: ")
    amount = float(input("Enter amount: "))
    record_type = input("Enter record type (income/expense): ")

    try:
        financial_record_service.add_financial_record(employee_id, description, amount, record_type)
    except FinancialRecordException as e:
        print(e)
        return

    print("Financial record added successfully.")
    
def view_financial_records(employee_service, financial_record_service):
    employee_id = int(input("Enter employee ID: "))
    try:
        employee = employee_service.get_employee_by_id(employee_id)
    except EmployeeNotFoundException as e:
        print(e)
        return

    financial_records = financial_record_service.get_financial_records_for_employee(employee_id)

    if not financial_records:
        print("No financial records found for this employee.")
        return

    print(f"\nFinancial Records for Employee {employee.first_name} {employee.last_name}:")
    for record in financial_records:
        print(f"\nRecord ID: {record.record_id}")
        print(f"Record Date: {record.record_date.isoformat()}")
        print(f"Description: {record.description}")
        print(f"Amount: {record.amount}")
        print(f"Record Type: {record.record_type}")
        
        
        
if __name__ == "__main__":
    main()
    
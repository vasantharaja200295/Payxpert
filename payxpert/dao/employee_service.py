# dao/employee_service.py
from abc import ABC, abstractmethod
from entity.employee import Employee
from exception.employee_not_found_exception import EmployeeNotFoundException

class IEmployeeService(ABC):
    @abstractmethod
    def get_employee_by_id(self, employee_id):
        pass

    @abstractmethod
    def get_all_employees(self):
        pass

    @abstractmethod
    def add_employee(self, employee_data):
        pass

    @abstractmethod
    def update_employee(self, employee_data):
        pass

    @abstractmethod
    def remove_employee(self, employee_id):
        pass

class EmployeeService(IEmployeeService):
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_employee_by_id(self, employee_id):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM Employee WHERE EmployeeID = %s"
        cursor.execute(query, (employee_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            employee = Employee(
                employee_id=result[0],
                first_name=result[1],
                last_name=result[2],
                date_of_birth=result[3],
                gender=result[4],
                email=result[5],
                phone_number=result[6],
                address=result[7],
                position=result[8],
                joining_date=result[9],
                termination_date=result[10]
            )
            return employee
        else:
            raise EmployeeNotFoundException(f"Employee with ID {employee_id} not found.")

    def get_all_employees(self):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM Employee"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        employees = []
        for result in results:
            employee = Employee(
                employee_id=result[0],
                first_name=result[1],
                last_name=result[2],
                date_of_birth=result[3],
                gender=result[4],
                email=result[5],
                phone_number=result[6],
                address=result[7],
                position=result[8],
                joining_date=result[9],
                termination_date=result[10]
            )
            employees.append(employee)

        return employees

    def add_employee(self, employee_data):
        cursor = self.db_connection.cursor()
        query = "INSERT INTO Employee (FirstName, LastName, DateOfBirth, Gender, Email, PhoneNumber, Address, Position, JoiningDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            employee_data.first_name,
            employee_data.last_name,
            employee_data.date_of_birth,
            employee_data.gender,
            employee_data.email,
            employee_data.phone_number,
            employee_data.address,
            employee_data.position,
            employee_data.joining_date
        )
        cursor.execute(query, values)
        self.db_connection.commit()
        cursor.close()

    def update_employee(self, employee_data):
        cursor = self.db_connection.cursor()
        query = "UPDATE Employee SET FirstName = %s, LastName = %s, DateOfBirth = %s, Gender = %s, Email = %s, PhoneNumber = %s, Address = %s, Position = %s, JoiningDate = %s, TerminationDate = %s WHERE EmployeeID = %s"
        values = (
            employee_data.first_name,
            employee_data.last_name,
            employee_data.date_of_birth,
            employee_data.gender,
            employee_data.email,
            employee_data.phone_number,
            employee_data.address,
            employee_data.position,
            employee_data.joining_date,
            employee_data.termination_date,
            employee_data.employee_id
        )
        cursor.execute(query, values)
        self.db_connection.commit()
        cursor.close()

    def remove_employee(self, employee_id):
        cursor = self.db_connection.cursor()
        query = "DELETE FROM Employee WHERE EmployeeID = %s"
        cursor.execute(query, (employee_id,))
        self.db_connection.commit()
        cursor.close()
# dao/tax_service.py
from abc import ABC, abstractmethod
from entity.tax import Tax
from exception.tax_calculation_exception import TaxCalculationException
from exception.employee_not_found_exception import EmployeeNotFoundException
from decimal import Decimal


class ITaxService(ABC):
    @abstractmethod
    def calculate_tax(self, employee_id, tax_year):
        pass

    @abstractmethod
    def get_tax_by_id(self, tax_id):
        pass

    @abstractmethod
    def get_taxes_for_employee(self, employee_id):
        pass

    @abstractmethod
    def get_taxes_for_year(self, tax_year):
        pass

class TaxService(ITaxService):
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def calculate_tax(self, employee_id, tax_year):
        cursor = self.db_connection.cursor()

        # Check if the employee exists
        query = "SELECT * FROM Employee WHERE EmployeeID = %s"
        cursor.execute(query, (employee_id,))
        employee = cursor.fetchone()

        if not employee:
            raise EmployeeNotFoundException(f"Employee with ID {employee_id} not found.")

        # Retrieve the employee's payrolls for the given tax year
        query = "SELECT SUM(NetSalary) AS TaxableIncome FROM Payroll WHERE EmployeeID = %s AND YEAR(PayPeriodEndDate) = %s"
        cursor.execute(query, (employee_id, tax_year))
        result = cursor.fetchone()

        if not result or result[0] is None:
            raise TaxCalculationException(f"No payroll records found for employee {employee_id} in the year {tax_year}.")

        taxable_income = result[0]

        tax_amount = taxable_income * Decimal('0.2')

        # Insert the tax record into the database
        query = "INSERT INTO Tax (EmployeeID, TaxYear, TaxableIncome, TaxAmount) VALUES (%s, %s, %s, %s)"
        values = (employee_id, tax_year, taxable_income, tax_amount)
        cursor.execute(query, values)
        self.db_connection.commit()
        cursor.close()

    def get_tax_by_id(self, tax_id):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM Tax WHERE TaxID = %s"
        cursor.execute(query, (tax_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            tax = Tax(
                tax_id=result[0],
                employee_id=result[1],
                tax_year=result[2],
                taxable_income=result[3],
                tax_amount=result[4]
            )
            return tax
        else:
            return None

    def get_taxes_for_employee(self, employee_id):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM Tax WHERE EmployeeID = %s"
        cursor.execute(query, (employee_id,))
        results = cursor.fetchall()
        cursor.close()

        taxes = []
        for result in results:
            tax = Tax(
                tax_id=result[0],
                employee_id=result[1],
                tax_year=result[2],
                taxable_income=result[3],
                tax_amount=result[4]
            )
            taxes.append(tax)

        return taxes

    def get_taxes_for_year(self, tax_year):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM Tax WHERE TaxYear = %s"
        cursor.execute(query, (tax_year,))
        results = cursor.fetchall()
        cursor.close()

        taxes = []
        for result in results:
            tax = Tax(
                tax_id=result[0],
                employee_id=result[1],
                tax_year=result[2],
                taxable_income=result[3],
                tax_amount=result[4]
            )
            taxes.append(tax)

        return taxes
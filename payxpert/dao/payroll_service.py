# dao/payroll_service.py
from abc import ABC, abstractmethod
from entity.payroll import Payroll
from exception.payroll_generation_exception import PayrollGenerationException
from exception.employee_not_found_exception import EmployeeNotFoundException

class IPayrollService(ABC):
    @abstractmethod
    def generate_payroll(self, employee_id, start_date, end_date):
        pass

    @abstractmethod
    def get_payroll_by_id(self, payroll_id):
        pass

    @abstractmethod
    def get_payrolls_for_employee(self, employee_id):
        pass

    @abstractmethod
    def get_payrolls_for_period(self, start_date, end_date):
        pass

class PayrollService(IPayrollService):
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def generate_payroll(self, employee_id, start_date, end_date):
        cursor = self.db_connection.cursor()

        # Check if the employee exists
        query = "SELECT * FROM Employee WHERE EmployeeID = %s"
        cursor.execute(query, (employee_id,))
        employee = cursor.fetchone()

        if not employee:
            raise EmployeeNotFoundException(f"Employee with ID {employee_id} not found.")

        # Calculate the payroll details (basic salary, overtime pay, deductions, etc.)
        # Implement your payroll calculation logic here
        basic_salary = 5000.0  # Example value, replace with your calculation
        overtime_pay = 500.0  # Example value, replace with your calculation
        deductions = 1000.0  # Example value, replace with your calculation
        net_salary = basic_salary + overtime_pay - deductions

        # Insert the payroll record into the database
        query = "INSERT INTO Payroll (EmployeeID, PayPeriodStartDate, PayPeriodEndDate, BasicSalary, OvertimePay, Deductions, NetSalary) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (employee_id, start_date, end_date, basic_salary, overtime_pay, deductions, net_salary)
        cursor.execute(query, values)
        self.db_connection.commit()
        cursor.close()

    def get_payroll_by_id(self, payroll_id):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM Payroll WHERE PayrollID = %s"
        cursor.execute(query, (payroll_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            payroll = Payroll(
                payroll_id=result[0],
                employee_id=result[1],
                pay_period_start_date=result[2],
                pay_period_end_date=result[3],
                basic_salary=result[4],
                overtime_pay=result[5],
                deductions=result[6],
                net_salary=result[7]
            )
            return payroll
        else:
            return None

    def get_payrolls_for_employee(self, employee_id):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM Payroll WHERE EmployeeID = %s"
        cursor.execute(query, (employee_id,))
        results = cursor.fetchall()
        cursor.close()

        payrolls = []
        for result in results:
            payroll = Payroll(
                payroll_id=result[0],
                employee_id=result[1],
                pay_period_start_date=result[2],
                pay_period_end_date=result[3],
                basic_salary=result[4],
                overtime_pay=result[5],
                deductions=result[6],
                net_salary=result[7]
            )
            payrolls.append(payroll)

        return payrolls

    def get_payrolls_for_period(self, start_date, end_date):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM Payroll WHERE PayPeriodStartDate >= %s AND PayPeriodEndDate <= %s"
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()
        cursor.close()

        payrolls = []
        for result in results:
            payroll = Payroll(
                payroll_id=result[0],
                employee_id=result[1],
                pay_period_start_date=result[2],
                pay_period_end_date=result[3],
                basic_salary=result[4],
                overtime_pay=result[5],
                deductions=result[6],
                net_salary=result[7]
            )
            payrolls.append(payroll)

        return payrolls
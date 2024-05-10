# dao/financial_record_service.py
from abc import ABC, abstractmethod
from entity.financial_record import FinancialRecord
from exception.financial_record_exception import FinancialRecordException
from exception.employee_not_found_exception import EmployeeNotFoundException

class IFinancialRecordService(ABC):
    @abstractmethod
    def add_financial_record(self, employee_id, description, amount, record_type):
        pass

    @abstractmethod
    def get_financial_record_by_id(self, record_id):
        pass

    @abstractmethod
    def get_financial_records_for_employee(self, employee_id):
        pass

    @abstractmethod
    def get_financial_records_for_date(self, record_date):
        pass

class FinancialRecordService(IFinancialRecordService):
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add_financial_record(self, employee_id, description, amount, record_type):
        cursor = self.db_connection.cursor()

        # Check if the employee exists
        query = "SELECT * FROM Employee WHERE EmployeeID = %s"
        cursor.execute(query, (employee_id,))
        employee = cursor.fetchone()

        if not employee:
            raise EmployeeNotFoundException(f"Employee with ID {employee_id} not found.")

        # Insert the financial record into the database
        query = "INSERT INTO FinancialRecord (EmployeeID, RecordDate, Description, Amount, RecordType) VALUES (%s, CURDATE(), %s, %s, %s)"
        values = (employee_id, description, amount, record_type)
        cursor.execute(query, values)
        self.db_connection.commit()
        cursor.close()

    def get_financial_record_by_id(self, record_id):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM FinancialRecord WHERE RecordID = %s"
        cursor.execute(query, (record_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            financial_record = FinancialRecord(
                record_id=result[0],
                employee_id=result[1],
                record_date=result[2],
                description=result[3],
                amount=result[4],
                record_type=result[5]
            )
            return financial_record
        else:
            return None

    def get_financial_records_for_employee(self, employee_id):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM FinancialRecord WHERE EmployeeID = %s"
        cursor.execute(query, (employee_id,))
        results = cursor.fetchall()
        cursor.close()

        financial_records = []
        for result in results:
            financial_record = FinancialRecord(
                record_id=result[0],
                employee_id=result[1],
                record_date=result[2],
                description=result[3],
                amount=result[4],
                record_type=result[5]
            )
            financial_records.append(financial_record)

        return financial_records

    def get_financial_records_for_date(self, record_date):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM FinancialRecord WHERE RecordDate = %s"
        cursor.execute(query, (record_date,))
        results = cursor.fetchall()
        cursor.close()

        financial_records = []
        for result in results:
            financial_record = FinancialRecord(
                record_id=result[0],
                employee_id=result[1],
                record_date=result[2],
                description=result[3],
                amount=result[4],
                record_type=result[5]
            )
            financial_records.append(financial_record)

        return financial_records
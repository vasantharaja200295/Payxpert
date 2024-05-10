# test_financial_record_service.py
import pytest
from datetime import date
from dao.financial_record_service import FinancialRecordService
from exception.employee_not_found_exception import EmployeeNotFoundException
from exception.financial_record_exception import FinancialRecordException
from util.db_conn_util import get_connection

@pytest.fixture
def financial_record_service():
    db_connection = get_connection()
    return FinancialRecordService(db_connection)

def test_add_financial_record(financial_record_service):
    employee_id = 1
    description = "Salary"
    amount = 5000.0
    record_type = "income"

    financial_record_service.add_financial_record(employee_id, description, amount, record_type)

    financial_records = financial_record_service.get_financial_records_for_employee(employee_id)
    assert len(financial_records) > 0
    latest_record = financial_records[-1]
    assert latest_record.employee_id == employee_id
    assert latest_record.description == description
    assert latest_record.amount == amount
    assert latest_record.record_type == record_type

def test_add_financial_record_for_invalid_employee(financial_record_service):
    invalid_employee_id = 999
    description = "Salary"
    amount = 5000.0
    record_type = "income"

    with pytest.raises(EmployeeNotFoundException):
        financial_record_service.add_financial_record(invalid_employee_id, description, amount, record_type)


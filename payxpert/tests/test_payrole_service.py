# test_payroll_service.py
import pytest
from datetime import date
from dao.payroll_service import PayrollService
from exception.employee_not_found_exception import EmployeeNotFoundException
from exception.payroll_generation_exception import PayrollGenerationException
from util.db_conn_util import get_connection

@pytest.fixture
def payroll_service():
    db_connection = get_connection()
    return PayrollService(db_connection)

def test_generate_payroll(payroll_service):
    employee_id = 1
    start_date = date(2023, 1, 1)
    end_date = date(2023, 1, 31)

    payroll_service.generate_payroll(employee_id, start_date, end_date)

    payrolls = payroll_service.get_payrolls_for_employee(employee_id)
    assert len(payrolls) > 0
    latest_payroll = payrolls[-1]
    assert latest_payroll.employee_id == employee_id
    assert latest_payroll.pay_period_start_date == start_date
    assert latest_payroll.pay_period_end_date == end_date
    assert latest_payroll.basic_salary > 0
    assert latest_payroll.overtime_pay >= 0
    assert latest_payroll.deductions >= 0
    assert latest_payroll.net_salary > 0

def test_generate_payroll_for_invalid_employee(payroll_service):
    invalid_employee_id = 999
    start_date = date(2023, 1, 1)
    end_date = date(2023, 1, 31)

    with pytest.raises(EmployeeNotFoundException):
        payroll_service.generate_payroll(invalid_employee_id, start_date, end_date)

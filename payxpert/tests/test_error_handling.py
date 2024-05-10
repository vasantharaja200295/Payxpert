import pytest
from dao.employee_service import EmployeeService
from dao.payroll_service import PayrollService
from exception.employee_not_found_exception import EmployeeNotFoundException
from exception.payroll_generation_exception import PayrollGenerationException
from datetime import date

@pytest.fixture
def services(db_connection):
    employee_service = EmployeeService(db_connection)
    payroll_service = PayrollService(db_connection)
    return employee_service, payroll_service

def test_handle_invalid_employee_data(services):
    employee_service, payroll_service = services
    
    # Try to generate payroll for a non-existent employee
    invalid_employee_id = 999
    start_date = date(2023, 1, 1)
    end_date = date(2023, 1, 31)

    with pytest.raises(EmployeeNotFoundException):
        payroll_service.generate_payroll(invalid_employee_id, start_date, end_date)

def test_handle_missing_payroll_data(services):
    employee_service, payroll_service = services
    
    # Get an employee
    employee = employee_service.get_employee_by_id(1)

    # Try to generate payroll for a period with no payroll data
    start_date = date(2023, 1, 1)
    end_date = date(2021, 12, 31)  # Past year with no payroll data

    with pytest.raises(PayrollGenerationException):
        payroll_service.generate_payroll(employee.employee_id, start_date, end_date)
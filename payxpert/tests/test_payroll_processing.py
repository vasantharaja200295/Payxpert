import pytest
from dao.employee_service import EmployeeService
from dao.payroll_service import PayrollService
from datetime import date

@pytest.fixture
def services(db_connection):
    employee_service = EmployeeService(db_connection)
    payroll_service = PayrollService(db_connection)
    return employee_service, payroll_service

def test_process_payroll_for_multiple_employees(services):
    employee_service, payroll_service = services
    
    # Get multiple employees
    employees = employee_service.get_all_employees()

    # Generate payrolls for all employees
    start_date = date(2023, 1, 1)
    end_date = date(2023, 1, 31)
    for employee in employees:
        payroll_service.generate_payroll(employee.employee_id, start_date, end_date)

    # Retrieve payrolls for the given period
    payrolls = payroll_service.get_payrolls_for_period(start_date, end_date)

    # Assert the number of payrolls generated
    expected_payroll_count = len(employees)
    assert expected_payroll_count == len(payrolls)
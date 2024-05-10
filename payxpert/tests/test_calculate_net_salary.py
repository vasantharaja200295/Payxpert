import pytest
from dao.employee_service import EmployeeService
from dao.payroll_service import PayrollService
from datetime import date

@pytest.fixture
def services(db_connection):
    employee_service = EmployeeService(db_connection)
    payroll_service = PayrollService(db_connection)
    return employee_service, payroll_service

def test_calculate_net_salary_after_deductions(services):
    employee_service, payroll_service = services
    
    # Get an employee
    employee = employee_service.get_employee_by_id(1)

    # Calculate payroll for the employee
    start_date = date(2023, 1, 1)
    end_date = date(2023, 1, 31)
    payroll_service.generate_payroll(employee.employee_id, start_date, end_date)

    # Retrieve the generated payroll record
    payrolls = payroll_service.get_payrolls_for_employee(employee.employee_id)
    payroll = payrolls[-1]  # Get the latest payroll record

    # Assert the net salary after deductions
    expected_net_salary = 4500.0
    assert expected_net_salary == payroll.net_salary
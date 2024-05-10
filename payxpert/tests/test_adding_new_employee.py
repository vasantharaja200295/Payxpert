import pytest
from datetime import date
from dao.employee_service import EmployeeService
from entity.employee import Employee
from exception.employee_not_found_exception import EmployeeNotFoundException
from util.db_conn_util import get_connection
@pytest.fixture
def employee_service():
    db_connection = get_connection()
    return EmployeeService(db_connection)

def test_get_employee_by_id(employee_service):
    employee_id = 1

    employee = employee_service.get_employee_by_id(employee_id)

    assert employee.employee_id == employee_id
    assert employee.first_name == "Vasantharaja"
    assert employee.last_name == "R"
    assert employee.date_of_birth == date(2002, 9, 5)

def test_get_employee_by_invalid_id(employee_service):
    invalid_employee_id = 999

    with pytest.raises(EmployeeNotFoundException):
        employee_service.get_employee_by_id(invalid_employee_id)

def test_add_employee(employee_service):

    new_employee = Employee(
        first_name="Jane",
        last_name="Smith",
        date_of_birth=date(1985, 9, 23),
        gender="F",
        email="jane.smith@example.com",
        phone_number="1234567890",
        address="123 Main St",
        position="Manager",
        joining_date=date(2022, 1, 1)
    )

    employee_service.add_employee(new_employee)

    added_employee = employee_service.get_employee_by_id(9)
    assert added_employee is not None


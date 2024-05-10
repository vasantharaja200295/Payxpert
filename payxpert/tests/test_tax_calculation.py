import pytest
from dao.employee_service import EmployeeService
from dao.tax_service import TaxService

@pytest.fixture
def services(db_connection):
    employee_service = EmployeeService(db_connection)
    tax_service = TaxService(db_connection)
    return employee_service, tax_service

def test_calculate_tax_for_high_income_employee(services):
    employee_service, tax_service = services
    
    # Get a high-income employee
    employee = employee_service.get_employee_by_id(2)

    # Calculate tax for the employee
    tax_year = 2023
    tax_service.calculate_tax(employee.employee_id, tax_year)

    # Retrieve the calculated tax record
    taxes = tax_service.get_taxes_for_employee(employee.employee_id)
    tax = next((t for t in taxes if t.tax_year == tax_year), None)

    # Assert the calculated tax amount
    expected_tax_amount = 25000.0
    assert tax is not None
    assert expected_tax_amount == tax.tax_amount
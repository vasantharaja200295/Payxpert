# test_tax_service.py
import pytest
from datetime import date
from dao.tax_service import TaxService
from exception.employee_not_found_exception import EmployeeNotFoundException
from exception.tax_calculation_exception import TaxCalculationException
from util.db_conn_util import get_connection

@pytest.fixture
def tax_service():
    db_connection = get_connection()
    return TaxService(db_connection)

def test_calculate_tax(tax_service):
    employee_id = 1
    tax_year = 2023

    tax_service.calculate_tax(employee_id, tax_year)

    taxes = tax_service.get_taxes_for_employee(employee_id)
    assert len(taxes) > 0
    latest_tax = taxes[-1]
    assert latest_tax.employee_id == employee_id
    assert latest_tax.tax_year == tax_year
    assert latest_tax.taxable_income > 0
    assert latest_tax.tax_amount > 0

def test_calculate_tax_for_invalid_employee(tax_service):
    invalid_employee_id = 999
    tax_year = 2023

    with pytest.raises(EmployeeNotFoundException):
        tax_service.calculate_tax(invalid_employee_id, tax_year)


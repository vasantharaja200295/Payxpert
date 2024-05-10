class Tax:
    def __init__(self, tax_id=None, employee_id=None, tax_year=None, taxable_income=None, tax_amount=None):
        self.tax_id = tax_id
        self.employee_id = employee_id
        self.tax_year = tax_year
        self.taxable_income = taxable_income
        self.tax_amount = tax_amount
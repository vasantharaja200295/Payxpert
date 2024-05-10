class FinancialRecord:
    def __init__(self, record_id=None, employee_id=None, record_date=None, description=None, amount=None, record_type=None):
        self.record_id = record_id
        self.employee_id = employee_id
        self.record_date = record_date
        self.description = description
        self.amount = amount
        self.record_type = record_type
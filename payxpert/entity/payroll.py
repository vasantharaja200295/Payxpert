class Payroll:
    def __init__(self, payroll_id=None, employee_id=None, pay_period_start_date=None, pay_period_end_date=None,
                 basic_salary=None, overtime_pay=None, deductions=None, net_salary=None):
        self.payroll_id = payroll_id
        self.employee_id = employee_id
        self.pay_period_start_date = pay_period_start_date
        self.pay_period_end_date = pay_period_end_date
        self.basic_salary = basic_salary
        self.overtime_pay = overtime_pay
        self.deductions = deductions
        self.net_salary = net_salary
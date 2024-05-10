# create_tables.py
import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="payrole"
)

cursor = db.cursor()

# Create the Employee table
create_employee_table = """
CREATE TABLE IF NOT EXISTS Employee (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    DateOfBirth DATE NOT NULL,
    Gender CHAR(1) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    PhoneNumber VARCHAR(20) NOT NULL,
    Address VARCHAR(200) NOT NULL,
    Position VARCHAR(100) NOT NULL,
    JoiningDate DATE NOT NULL,
    TerminationDate DATE
)
"""

# Create the Payroll table
create_payroll_table = """
CREATE TABLE IF NOT EXISTS Payroll (
    PayrollID INT AUTO_INCREMENT PRIMARY KEY,
    EmployeeID INT NOT NULL,
    PayPeriodStartDate DATE NOT NULL,
    PayPeriodEndDate DATE NOT NULL,
    BasicSalary DECIMAL(10, 2) NOT NULL,
    OvertimePay DECIMAL(10, 2) NOT NULL,
    Deductions DECIMAL(10, 2) NOT NULL,
    NetSalary DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
)
"""

# Create the Tax table
create_tax_table = """
CREATE TABLE IF NOT EXISTS Tax (
    TaxID INT AUTO_INCREMENT PRIMARY KEY,
    EmployeeID INT NOT NULL,
    TaxYear YEAR NOT NULL,
    TaxableIncome DECIMAL(10, 2) NOT NULL,
    TaxAmount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
)
"""

# Create the FinancialRecord table
create_financial_record_table = """
CREATE TABLE IF NOT EXISTS FinancialRecord (
    RecordID INT AUTO_INCREMENT PRIMARY KEY,
    EmployeeID INT NOT NULL,
    RecordDate DATE NOT NULL,
    Description VARCHAR(200) NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    RecordType VARCHAR(50) NOT NULL,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
)
"""

# Execute the table creation queries
cursor.execute(create_employee_table)
cursor.execute(create_payroll_table)
cursor.execute(create_tax_table)
cursor.execute(create_financial_record_table)

# Commit the changes and close the connection
db.commit()
cursor.close()
db.close()
from db import get_connection

tables = [

"""
CREATE TABLE Users(
    id INT PRIMARY KEY IDENTITY(1,1),
    username VARCHAR(50),
    password VARCHAR(100)
)
""",

"""
CREATE TABLE Expenses(
    id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT,
    title VARCHAR(100),
    category VARCHAR(50),
    amount FLOAT,
    expense_date DATE
)
""",

"""
CREATE TABLE Budget(
    id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT,
    monthly_budget FLOAT
)
""",

"""
CREATE TABLE Investments(
    id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT,
    investment_name VARCHAR(100),
    amount FLOAT
)
"""

]

conn = get_connection()
cursor = conn.cursor()

for table in tables:
    try:
        cursor.execute(table)
        conn.commit()
        print("✅ Table created")
    except Exception as e:
        print(e)

cursor.close()
conn.close()
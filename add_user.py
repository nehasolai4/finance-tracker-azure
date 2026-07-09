from db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
INSERT INTO Users(username,password)
VALUES(?,?)
""",("admin","admin124"))

conn.commit()

print("User added!")

cursor.close()
conn.close()
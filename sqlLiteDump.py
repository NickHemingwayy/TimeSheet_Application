import mysql.connector
import os
import _sqlite3
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
database = os.getenv('DATABASE')

conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
cursor = conn.cursor()

cursor.execute('''
                        SELECT * FROM department

                      ''')
result = cursor.fetchall()
#print(result)

conn = _sqlite3.connect(r'C:\Users\nhemingway\PycharmProjects\TimeSheet\TimeSheet.db')
c = conn.cursor()

recs = c.execute('''
                            SELECT dep_name, legalent_name, task_name, customer, hours, dateworked
                                        FROM timesheet
                                        WHERE employee = ? AND dateworked BETWEEN ? AND ?; 
                          ''', ('nhemingway','2021','2022'))
for rec in recs:
    print(rec)
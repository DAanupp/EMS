import mysql.connector

conn=mysql.connector.connect( 
    host='localhost',
    user='root',
    password='sql123',
    database='ems'
)

cur=conn.cursor()
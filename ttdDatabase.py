import mysql.connector
import serial


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="ttdDatabase"
)

mydb.autocommit = True
mycursor = mydb.cursor()

ser = serial.Serial("COM3", 9600)

while True:
    line = ser.readline().decode().strip()  # Read and clean the data

    # Only process lines that start with "Ticket Verification Number:"
    if line.startswith("Ticket Verification Number:"):
        ticket_number = line.split(":")[1].strip()  # Extract number
        print(f"Extracted Ticket: {ticket_number}")  # Only print ticket numbers

        sqlFormula = "INSERT INTO ticket (number) VALUES (%s)"
        mycursor.execute(sqlFormula, (ticket_number,))






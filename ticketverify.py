import mysql.connector
import serial

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="ttdDatabase"
)

mycursor = mydb.cursor()

# Connect to Arduino Serial Port
ser = serial.Serial("COM3", 9600)  # Change to your Arduino COM port

def verify_ticket(ticket_number):
    """Checks if the ticket number exists in the database"""
    sqlFormula = "SELECT * FROM ticket WHERE number = %s"
    mycursor.execute(sqlFormula, (ticket_number,))
    result = mycursor.fetchone()  # Fetch one matching record

    if result:
        print(f"✅ Ticket {ticket_number} is VALID.")
    else:
        print(f"❌ Ticket {ticket_number} is INVALID.")

while True:
    line = ser.readline().decode().strip()  # Read from Arduino
    if line.startswith("Ticket Verification Number:"):
        ticket_number = line.split(":")[1].strip()  # Extract ticket number
        print(f"Extracted Ticket: {ticket_number}")  # Debugging
        verify_ticket(ticket_number)  # Verify ticket

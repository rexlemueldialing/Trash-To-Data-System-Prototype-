import mysql.connector
import serial
import time

# Establish MySQL connection
def connect_to_database():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="ttdDatabase"
        )
        db.autocommit = True  # Enable auto-commit
        print("Database connection successful")
        return db
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

# Establish Serial Connection
def connect_to_serial():
    try:
        ser = serial.Serial("COM3", 9600, timeout=2)
        print("Serial connection established")
        return ser
    except serial.SerialException as err:
        print(f"Error opening serial port: {err}")
        return None

# Main function
def main():
    mydb = connect_to_database()
    ser = connect_to_serial()

    if not mydb or not ser:
        print("Failed to establish connections. Exiting...")
        return

    mycursor = mydb.cursor()

    while True:
        try:
            line = ser.readline().decode().strip()  # Read and clean the data
            if line:
                print(f"Received: {line}")  # Show all received data

            if line.startswith("Ticket Verification Number:"):
                ticket_number = line.split(":")[1].strip()  # Extract number
                print(f"Extracted Ticket: {ticket_number}")  # Show only extracted ticket

                sqlFormula = "INSERT INTO sendticket (basket1) VALUES (%s)"
                mycursor.execute(sqlFormula, (ticket_number,))
                print("Ticket inserted successfully")

        except serial.SerialException as se:
            print(f"Serial Error: {se}")
            time.sleep(2)  # Wait before retrying

        except mysql.connector.Error as me:
            print(f"MySQL Error: {me}")
            mydb = connect_to_database()  # Attempt to reconnect to DB
            if mydb:
                mycursor = mydb.cursor()

        except KeyboardInterrupt:
            print("Program terminated by user")
            break

    ser.close()
    mydb.close()

if __name__ == "__main__":
    main()

import mysql.connector
import serial
import time

def connect_to_database():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="ttdDatabase"
        )
        db.autocommit = True
        print("Database connection successful")
        return db
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def connect_to_serial():
    try:
        ser = serial.Serial("COM3", 9600, timeout=2)
        print("Serial connection established")
        return ser
    except serial.SerialException as err:
        print(f"Error opening serial port: {err}")
        return None

def main():
    mydb = connect_to_database()
    ser = connect_to_serial()

    if not mydb or not ser:
        print("Failed to establish connections. Exiting...")
        return

    mycursor = mydb.cursor()

    while True:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode().strip()
                print(f"Received: {line}")  # Debug: Show all incoming data

                # Parse structured messages
                if line.startswith("TICKET:"):
                    ticket_data = line.split(":")[1].split(",")
                    ticket_number = ticket_data[0]
                    weight = ticket_data[1] if len(ticket_data) > 1 else "0"
                    
                    print(f"Ticket: {ticket_number}, Weight: {weight}g")
                    mycursor.execute("INSERT INTO ticket (number, weight) VALUES (%s, %s)", (ticket_number, weight))

                elif line.startswith("WEIGHT:"):
                    weight = line.split(":")[1]
                    print(f"Current Weight: {weight}g")

                elif line == "PLASTIC_DETECTED":
                    print("Plastic detected!")

                elif line.startswith("System"):
                    print(f"System Status: {line}")

        except serial.SerialException as se:
            print(f"Serial Error: {se}")
            time.sleep(2)

        except mysql.connector.Error as me:
            print(f"MySQL Error: {me}")
            mydb = connect_to_database()  # Reconnect
            if mydb:
                mycursor = mydb.cursor()

        except KeyboardInterrupt:
            print("Program terminated by user")
            break

    ser.close()
    mydb.close()

if __name__ == "__main__":
    main()
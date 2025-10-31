import serial

ser = serial.Serial("COM3", 9600)  # Change COM port if needed

while True:
    line = ser.readline().decode().strip()  # Read and clean the data

    # Only process lines that start with "Ticket Verification Number:"
    if line.startswith("Ticket Verification Number:"):
        ticket_number = line.split(":")[1].strip()  # Extract number
        print(f"Extracted Ticket: {ticket_number}")  # Only print ticket numbers
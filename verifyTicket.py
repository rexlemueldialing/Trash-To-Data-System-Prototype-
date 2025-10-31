import mysql.connector

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",   # Change if necessary
    passwd="root", # Change if necessary
    database="ttdDatabase"
)

mycursor = mydb.cursor()

# Function to verify ticket number
def verify_ticket(ticket_number):
    sql_query = "SELECT * FROM ticket WHERE number = %s"
    mycursor.execute(sql_query, (ticket_number,))
    result = mycursor.fetchone()  # Get the first matching result

    if result:
        print(f"VERIFIED")
    else:
        print(f"INVALID4943767")

# Ask user for ticket number
ticket_number = input("Enter Ticket Number: ")
verify_ticket(ticket_number)

# Close connection
mycursor.close()
mydb.close()

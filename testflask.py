from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="ttdDatabase"
)
cursor = db.cursor()

# Route to retrieve all tickets
@app.route('/tickets', methods=['GET'])
def get_tickets():
    cursor.execute("SELECT * FROM ticket")
    tickets = cursor.fetchall()  # Fetch all ticket numbers
    return jsonify(tickets)

# Route to verify a ticket
@app.route('/verify', methods=['POST'])
def verify_ticket():
    data = request.json
    ticket_number = data.get("ticket_number")

    cursor.execute("SELECT * FROM ticket WHERE number = %s", (ticket_number,))
    ticket = cursor.fetchone()

    if ticket:
        return jsonify({"status": "valid", "ticket_number": ticket_number})
    else:
        return jsonify({"status": "invalid", "ticket_number": ticket_number})

if __name__ == '__main__':
    app.run(debug=True)  
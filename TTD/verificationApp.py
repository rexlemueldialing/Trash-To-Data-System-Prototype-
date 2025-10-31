from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="ttdDatabase"
    )

@app.route('/')
def home():
    return render_template('index.html')  # Loads the HTML form

@app.route('/verify', methods=['POST'])
def verify_ticket():
    ticket_number = request.form.get("ticket_number")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sendticket WHERE basket1 = %s", (ticket_number,))
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    if result:
        return render_template('verify.html', message=f"✅ Ticket {ticket_number} is VERIFIED!")
    else:
        return render_template('verify.html', message=f"❌ Ticket {ticket_number} is INVALID!")

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
from datetime import date
import sqlite3
import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Dictionary to hold real-time bookings
bookings = {
    'court1': {},
    'court2': {}
}
dates = {}

def get_db_connection():
    conn = sqlite3.connect('sportcenter.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insert')
def insert():
    return render_template('insert.html')

@app.route('/insert_paddle', methods=['POST'])
def insert_paddle():
    id_number = request.form['id_number']
    facility = request.form['court']
    hour = request.form['time']
    current_date = date.today().isoformat()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT facility, date, hour 
        FROM sportcenter 
        WHERE facility = ? AND date = ? AND hour = ?
    """, (facility, current_date, hour))
    reserved = cursor.fetchone()
    
    if reserved:
        message = 'Sorry but this court is already booked, click on refresh bookings to see free hours'
        return render_template('index.html', message=message)
    else:
        message = 'Your booking is done!'
        db.insert_db(id_number, facility, hour)
        # Update bookings dictionary and notify clients
        bookings[facility][hour] = 'booked'
        emit('booking_update', bookings, broadcast=True)
        
        return render_template('t.html', message=message)


def load_bookings_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT facility, hour FROM sportcenter")
    rows = cursor.fetchall()
    for row in rows:
        facility, hour = row
        if facility not in bookings:
            bookings[facility] = {}
        bookings[facility][hour] = 'booked'
    
    conn.close()

@socketio.on('connect')
def handle_connect():
    # When a client connects, load bookings from the DB and send them
    load_bookings_from_db()
    emit('booking_update', bookings, broadcast=True)

@socketio.on('book')
def handle_booking(data):
    id_number = data['id_number']
    court = data['facility']
    time_slot = data['hour']
    
    # Insert booking into the database
    db.insert_db(id_number, court, time_slot)
    
    # Update bookings dictionary
    bookings[court][time_slot] = 'booked'
    
    # Notify all clients about the booking
    emit('booking_update', bookings, broadcast=True)

if __name__ == '__main__':
    db.create_db()
    socketio.run(app, debug=True)

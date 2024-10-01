from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
from datetime import date
import sqlite3
import db
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
@app.route('/')
def index():
    return render_template('index.html', vector=[])

@app.route('/insert')
def insert():
    return render_template('insert.html', vector=[])


@app.route('/insert_paddle', methods=['POST'])
def insert_paddle ():
    id_number = request.form['id_number']
    facility = request.form['court']
    hour = request.form['time']
    current_date = date.today().isoformat()
    conexion = sqlite3.connect('sportcenter.db')
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT facility, date, hour 
        FROM sportcenter 
        WHERE facility = ? AND date = ? AND hour = ?
    """, (facility, current_date, hour))
    reserved = cursor.fetchone()
    if(reserved):
        message = 'Sorry but this court is already booked, click on refresh bookings to see free hours'
        return render_template('index.html', vector=[], message = message)
    else:
        message = 'your booking is done!'
        db.insert_db(id_number, facility, hour)
        return render_template('t.html', vector=[], message = message)
    


@app.route('/court1_get_bookings_paddle', methods=['GET'])
def court1_get_bookings_paddle():
    conexion = sqlite3.connect('sportcenter.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT hour FROM sportcenter WHERE facility = 'court1'")    
    vector = [fila[0] for fila in cursor.fetchall()]  
    conexion.close()
    return render_template('index.html', vector = vector)

@app.route('/court2_get_bookings_paddle', methods=['GET'])

def court2_get_bookings_paddle():
    conexion = sqlite3.connect('sportcenter.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT hour FROM sportcenter WHERE facility = 'Court 2'")    
    vector = [fila[0] for fila in cursor.fetchall()]  
    conexion.close()
    return render_template('index.html', vector = vector)

# Data that represents the current bookings
bookings = {
    'court1': {},
    'court2': {}
}

def get_db_connection():
    conn = sqlite3.connect('sportcenter.db')
    conn.row_factory = sqlite3.Row
    return conn

@socketio.on('connect')
def handle_connect():
    # When a client connects, send the current booking status
    emit('booking_update', bookings, broadcast=True)

@socketio.on('book')
def handle_booking(data):
    court = data['facility']
    time_slot = data['hour']
    bookings[court][time_slot] = 'booked'
    
    # Notify all clients that a booking has been made
    emit('booking_update', bookings, broadcast=True)



def get_db_connection():
    conn = sqlite3.connect('sportcenter.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ejecutar la aplicación con WebSockets
if __name__ == '__main__':
    db.create_db()  # Asegúrate de que esto se ejecuta solo una vez.
    socketio.run(app, debug=True)
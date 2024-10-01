from flask import Flask, request, render_template
from datetime import date
import sqlite3

def create_db():
    conexion = sqlite3.connect('sportcenter.db')
    cursor = conexion.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sportcenter(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_number INT NOT NULL,
        facility TEXT NOT NULL,
        date TEXT NOT NULL,
        hour TEXT NOT NULL
    )
    ''')
    conexion.commit()
    conexion.close()

def insert_db(id_number, facility, hour):
    conexion = sqlite3.connect('sportcenter.db')
    cursor = conexion.cursor()
    current_date = date.today().isoformat()
    cursor.execute('''INSERT INTO sportcenter(id_number, facility, date, hour) VALUES(?,?,?,?)
    ''', (id_number, facility, current_date, hour))
    conexion.commit()
    conexion.close()




import mysql.connector
import streamlit as st

def create_connection():
    conn = mysql.connector.connect(
        host="localhost",      
        user="root",  
        password="",  
        database="license_plate_app"  
    )
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS license_plates (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        license_plate_number VARCHAR(255),
                        video_path VARCHAR(255),
                        frame_no int,
                        coordinates VARCHAR(255),
                        timestamp VARCHAR(255)
                     )''')
    conn.commit()
    conn.close()
    
def insert_license_plate(license_plate_number, video_path, frame_no, coordinates, timestamp):
    conn = create_connection()
    cursor = conn.cursor()
    
    insert_query = '''INSERT INTO license_plates (license_plate_number, video_path, frame_no, coordinates, timestamp)
                      VALUES (%s, %s, %s, %s, %s)'''
    
    data = (license_plate_number, video_path, frame_no, coordinates, timestamp)
    
    cursor.execute(insert_query, data)
    conn.commit()
    conn.close()

def get_car(license_number):
    conn = create_connection()
    cursor = conn.cursor()
    
    select_query = '''SELECT * FROM license_plates WHERE license_plate_number = %s'''
    cursor.execute(select_query, (license_number,))
    result = cursor.fetchall()
    conn.close()
    return [entry for entry in result]

def check_entry_exists(video_path):
    conn = create_connection()
    cursor = conn.cursor()
    
    select_query = '''SELECT * FROM license_plates WHERE video_path = %s'''
    cursor.execute(select_query, (video_path,))
    result = cursor.fetchall()
    conn.close()
    return len(result) > 0
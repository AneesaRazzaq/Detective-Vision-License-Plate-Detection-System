import streamlit as st
from PIL import Image
import io
import os
import cv2
import ast
from number_plate_detection import detect_license_plate
from database import create_table
from database import insert_license_plate, check_entry_exists
from database import get_car


create_table()

st.header('Give the Folder Path of Car Videos')
videos_path = st.text_input('Enter path to the Video directory')
    
    
if st.button('Process Videos'):
    video_folders_list = os.listdir(videos_path)
    print(f'--------------------{video_folders_list}')
    
    for video_folder in video_folders_list:
        video_name = os.listdir(os.path.join(videos_path, video_folder))[0]
        print(f'--------------------{video_name}')
        video_path = os.path.join(videos_path, video_folder, video_name)
        if not check_entry_exists(video_path):
            detected_number, detected_plate = detect_license_plate(video_path)
            
            # Check if detected_plate is not None
            if detected_plate is not None:
                print(detected_plate[0])

                # Or if you're specifically after the coordinates:
                frame_no = detected_plate[0]
                number_plate_coordinates = detected_plate[1]
                print(f"Frame number: {frame_no}, Coordinates: {number_plate_coordinates}")
                
                # For Streamlit output:
                st.write(f"Detected plate at Frame {frame_no} with Coordinates: {number_plate_coordinates}")
                
                # Insert into the database
                if insert_license_plate(detected_number, video_path, frame_no, str(number_plate_coordinates), '2022-01-01 00:00:00'):
                    st.write('Saved in the database')
                
            else:
                # If no plate is detected, log it or show a message
                st.write(f"No license plate detected for video: {video_path}")
        else:
            st.write('Already in the database')

            

st.header('Find Car')
license_number = st.text_input('Enter the Car license number')
if st.button('Find Car'):
    if license_number:
        car_entries = get_car(license_number)
        for car in car_entries:
            
            id , license_number, video_path, frame_no, coordinates, timestamp = car
            video = cv2.VideoCapture(video_path)
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ret, frame = video.read()
            coordinates_touple = ast.literal_eval(coordinates)
            x1, y1, x2, y2 = coordinates_touple
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame,license_number ,(int(x1), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            
            cropped_timestamp = frame[0:100, 850:1280]
        

            st.image(frame)
            st.image(cropped_timestamp)

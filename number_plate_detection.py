from ultralytics import YOLO
from collections import defaultdict
from collections import Counter
import easyocr
import cv2
from statistics import mode

def detect_license_plate(video_path):
    # Load pre-trained YOLO model
    model = YOLO('F:\\knowledge_stream\\datascienceKnowledgeStream\\final mini project number plate detection\\license_plate_detector.pt')

    video = cv2.VideoCapture(video_path)
    detected_plates = defaultdict(list)
    detected_numbers = []
    
    reader = easyocr.Reader(['en'])
    preds = ['']
    
    while True:
        ret, frame = video.read()
        if not ret:
            break

        frame_no = int(video.get(cv2.CAP_PROP_POS_FRAMES))
        
        # Run YOLO model on the frame
        results = model(frame)

        res = ""  # Initialize res to an empty string or a default value

        for result in results[0].boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            number_plate_coordinates = (x1, y1, x2, y2)
            print(score, x1, y1, x2, y2)

            # Crop the detected vehicle region
            car_crop = frame[int(y1):int(y2), int(x1):int(x2)]
            gray_car = cv2.cvtColor(car_crop, cv2.COLOR_BGR2GRAY)

            result = reader.readtext(gray_car)

            ocr_res = []
            for k in range(len(result)):
                if (result[k][2]) > 0.3 and len(result[k][1]) > 2:
                    ocr_res.append(result[k][1])
            ocr_res = ''.join(ocr_res)
            print(result, ocr_res, '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            
            if len(ocr_res) > 1:
                preds.append(ocr_res.upper())
                res = mode(preds)
                detected_plates[ocr_res.upper().strip()].append((frame_no, number_plate_coordinates))
            
            # Only try to print res if it's not empty or None
            if res:
                print(f"Frame {frame_no} - License Plate: {res.strip()}")
            else:
                print(f"Frame {frame_no} - No License Plate detected.")
                
        # Optionally display the frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Process after the video loop
    number_counts = Counter(preds)
    most_common_number, occurrences = number_counts.most_common(1)[0]

    # Check if detected_plates contains the most_common_number
    if most_common_number in detected_plates and detected_plates[most_common_number]:
        # Rewind video to the first frame for cropping (ensure video has valid frames left)
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = video.read()
        
        if frame is not None:
            cv2.imwrite('frame', frame)
            cropped_timestamp = frame[0:100, 850:1280]

            gray_cropped = cv2.cvtColor(cropped_timestamp, cv2.COLOR_BGR2GRAY)

            cv2.imshow('frame', cropped_timestamp)
            return mode(preds), detected_plates[most_common_number][0]
        else:
            print("No valid frame to crop after rewinding.")
            return mode(preds), detected_plates[most_common_number][0]
    else:
        print("No license plates detected.")
        return None, None  # Handle the case where no plates were detected

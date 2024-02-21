# Import necessary libraries
import math
import cv2  # OpenCV for image processing
import numpy as np  # NumPy for numerical operations
import mediapipe as mp  # MediaPipe for face detection
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os  # OS module for environment variables and file operations
import serial  # Serial library for communication with external devices

# Setup serial communication with STM32 microcontroller(uart communication)
STM32 = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.01)

# Disable CUDA to force TensorFlow/MediaPipe to use CPU
os.environ['CUDA_VISIBLE_DEVICES'] = ''

# Initialize a point variable to store the detected face point
point = (0, 0)

# Configure the face detection model
base_options = python.BaseOptions(model_asset_path='detector.tflite')
options = vision.FaceDetectorOptions(base_options=base_options, min_detection_confidence=0.7)
detector = vision.FaceDetector.create_from_options(options)

# Flag to indicate if a face has been detected
flag = 0

def _normalized_to_pixel_coordinates(normalized_x: float, normalized_y: float, image_width: int, image_height: int):
    """Convert normalized coordinates to pixel coordinates."""
    def is_valid_normalized_value(value: float) -> bool:
        """Check if the normalized value is within [0.0, 1.0]."""
        return (value > 0 or math.isclose(0, value)) and (value < 1 or math.isclose(1, value))
    
    if not (is_valid_normalized_value(normalized_x) and is_valid_normalized_value(normalized_y)):
        return None
    
    x_px = min(math.floor(normalized_x * image_width), image_width - 1)
    y_px = min(math.floor(normalized_y * image_height), image_height - 1)
    return x_px, y_px

def visualize(image, detection_result):
    """Visualize the detection results on the image."""
    global point
    global flag
    annotated_image = image.copy()
    height, width, _ = image.shape
    
    # Handling multiple or single face detection cases
    if len(detection_result.detections) > 1:
        print('there is more than one face')
    elif len(detection_result.detections) == 1:
        detection = detection_result.detections[0]
        if detection.keypoints:
            flag = 1
            keypoint = detection.keypoints[2]
            keypoint_px = _normalized_to_pixel_coordinates(keypoint.x, keypoint.y, width, height)
            point = keypoint_px
            
            # Drawing a circle and crosshair on the detected face point
            color, thickness, radius = (0, 255, 0), 2, 2
            cv2.circle(annotated_image, keypoint_px, thickness, color, radius)
            horizontal_start = (0, point[1])
            horizontal_end = (width - 1, point[1])
            cv2.line(annotated_image, horizontal_start, horizontal_end, (255, 255, 0), 2)
            vertical_start = (point[0], 0)
            vertical_end = (point[0], height - 1)
            cv2.line(annotated_image, vertical_start, vertical_end, (255, 255, 0), 2)
    else:
        pass  # Do nothing if no faces are detected
    return annotated_image

# Main execution block
try:
    # Setup video capture and output
    cap = cv2.VideoCapture(2)
    out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, (640, 480))
    test = ""
    
    # Main loop for video processing
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imwrite('frame.jpg', frame)
        image = mp.Image.create_from_file('frame.jpg')
        detection_result = detector.detect(image)
        image_copy = np.copy(image.numpy_view())
        
        annotated_image = visualize(image_copy, detection_result)
        
        # Encoding the face point coordinates for serial transmission
        if (point[0] // 100) == 0:
            test = '0' + str(point[0])
        else:
            test = str(point[0])
        if (point[1] // 100) == 0:
            test = test + '0' + str(point[1])
        else:
            test = test + str(point[1])
        if len(test) != 6 or flag == 0: 
            test = '320240'
        STM32.write(test.encode('utf-8'))
        
        annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
        out.write(annotated_image)
        # Uncomment below to display the annotated video in real-time
        # cv2.imshow('Face Recognition', annotated_image)
        
        flag = 0
        if cv2.waitKey(1) & 0xFF == 27:  # Break loop if 'Esc' key is pressed
            break
except Exception as e:
    print("An error occurred:", str(e))
finally:
    # Cleanup resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    os.remove('frame.jpg')  # Delete the temporary frame image
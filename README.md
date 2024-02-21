# Face Tracker
![1](https://github.com/AHMED-BELKHIRI/Face-Tracker/assets/90837035/986083e8-6c60-4ecc-9a22-e97e87359b29)
## Project Overview

The Face Tracking Camera System is a solution designed to dynamically track human faces using a camera module, interfaced with an STM32 microcontroller and controlled via two servo motors. This project aims to keep the detected face centered in the camera's view, regardless of movement, making it ideal for applications in security, user interaction, and automated monitoring systems.

## Key Components and Features

- **STM32F446RE Board:** At the heart of the FACE TRACKER is the STM32 microcontroller, which orchestrates the movement and tracking process. It processes incoming X and Y position commands via UART serial communication, ensuring precise control over the tracking mechanism.
- **Raspberry Pi 4:**  Serving as the brains behind the image processing, the Raspberry Pi 4 is tasked with detecting faces within the video feed. It calculates the central point of detected faces and communicates these coordinates to the STM32 microcontroller via UART, enabling dynamic tracking.

- **Servo Motors (Super Gear):** Precision is key in the FACE TRACKER's design, which is why each joint utilizes a high-quality servo motor. These motors provide the necessary controlled and accurate rotational motion, ensuring the face remains centered in the frame with high precision.

- **Required Libraries in`requirements.txt`:** Essential to the project's Python-based face detection algorithm, the requirements.txt file lists all necessary libraries that must be installed. This file streamlines the setup process, ensuring all dependencies are met for successful execution.

- **Movement Algorithm in `main.cp`:** The core of the FACE TRACKER's motion control lies within the main.c source file, which implements a PID controller algorithm. This sophisticated algorithm adjusts the servo motors to accurately position based on the received X and Y coordinates over the serial port. The source code for this algorithm can be found in the tracker/Core/Src directory.

## Getting Started

To explore and adapt this project for your needs, follow these steps:
1. Download and install STM32CubeIDE from the STMicroelectronics website.
2. Configure the IDE to recognize your specific STM32 board model. Detailed instructions can be found in the IDE’s documentation.
3. Understanding the PID Control Algorithm
4. Install Python Dependencies:
   `pip insatll -r requirements.txt`
   
   `wget -q -O detector.tflite -q https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite`
6. Edit the face_tracker.py script to set the correct camera address and STM32 serial port according to your setup.
7. Upload the adjusted code to your STM32 board.
8. Ensure the robotic Face Tracker hardware is correctly connected and powered.
9. Execute the face tracking script by navigating to the script's directory and running:
   `python3 face_tracker.py`

   Make sure to replace /path/to/your/face_tracker/file/ with the actual path to the face_tracker.py script.

## Mechanical Overview
The mechanical design of the Face Tracker robot was meticulously crafted using SolidWorks 2022, ensuring precision and durability. For those interested in exploring the mechanical aspects of the project, including detailed part designs and assembly instructions, we have made all the relevant files available on GrabCAD.
`https://grabcad.com/library/face-tracker-1`

## Python Code Overview
The Python segment of our project leverages the powerful capabilities of the MediaPipe library for real-time face detection. By utilizing this library, we efficiently detect faces within the video feed and accurately determine the localization of each face's midpoint. This critical information, specifically the coordinates of the detected face's center, is then transmitted to the STM32 microcontroller via UART (Universal Asynchronous Receiver-Transmitter) communication. This process ensures seamless data flow and integration between the computational analysis performed by the Raspberry Pi and the mechanical actions executed by the STM32 microcontroller, forming the backbone of our face-tracking functionality.

## C Code Overview
On the C programming front, the project employs a sophisticated PID (Proportional, Integral, Derivative) control algorithm. This algorithm is crucial for the precise control of the servo motors, enabling them to adjust and maintain the camera's focus on the detected face's midpoint. To enhance efficiency and responsiveness, data transmission between the Raspberry Pi and the STM32 microcontroller is facilitated through UART communication, incorporating UART interrupts to minimize processing delays. Furthermore, the calculation of the PWM (Pulse Width Modulation) signals, essential for controlling the servo motors, is executed within the UART interrupt callback function. This approach not only optimizes the system's reaction time to the dynamic input from the Python code but also ensures that the servo motors can swiftly and accurately reach the desired positions, maintaining the face centered in the camera's field of view.


For questions or assistance, contact me at belkhiri.ahmedd@gmail.com .

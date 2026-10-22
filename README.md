# OpenCV + ESP32 Expression Detector

## Overview

A computer vision project that uses Python, OpenCV, and MediaPipe to detect facial expressions through a webcam and communicate the detected expression to an ESP32, which displays it on a 16×2 LCD.

## Features

- Webcam-based face landmark detection
- Smile detection using MediaPipe face blendshape scores
- Serial communication between Python and ESP32
- Real-time expression display on a 16×2 LCD

## Technologies

- Python
- OpenCV
- MediaPipe Tasks
- PySerial
- ESP32
- Arduino C++
- 16×2 LCD

## How It Works

1. The webcam captures a video frame.
2. MediaPipe detects facial landmarks and estimates smile-related blendshape scores.
3. Python classifies the expression using a threshold.
4. Python sends the expression to the ESP32 over serial communication.
5. The ESP32 receives the message and updates the LCD.

## Hardware

- ESP32 development board
- 16×2 LCD
- USB cable
- Computer with a webcam
- Jumper wires and suitable LCD power/contrast connections

## Setup

1. Install Python and the Arduino IDE.
2. Install the Python dependencies listed in `requirements.txt`.
3. Download the compatible MediaPipe Face Landmarker model and place it at the path expected by the Python script.
4. Connect the LCD to the ESP32 using the pin mapping documented in the Arduino sketch.
5. Upload the ESP32 sketch.
6. Configure the correct serial port in the Python script.
7. Run `main.py` and test the expression display.

## Learning Outcomes

- Computer vision and facial landmark detection
- Serial communication between Python and a microcontroller
- Embedded programming
- Sensor-data interpretation and threshold-based classification
- Hardware/software integration and debugging

## Future Improvements

- Add more expression categories
- Smooth expression scores to reduce flickering
- Add communication acknowledgements and error handling
- Improve configuration so the serial port and model path are easy to change

## Status

Working prototype; further testing and improvements are ongoing.

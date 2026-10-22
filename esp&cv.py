
import cv2 #It allows access to the openCV library
import mediapipe as mp #It imports mediapipe & gives it a short name mp
import time #It measures elapsed time for video timestamps
from mediapipe.tasks import python #It gives access to MediaPipe's configuration tools
from mediapipe.tasks.python import vision #It gives access to vision tools, including the landmark face detector
import serial #Allows serial communication between the laptop and the micro controller


# 1. Configure serial communication with the ESP32
ESP32_PORT = "COM14"  
BAUD_RATE = 9600

#This creates a serial connection object and attempts to open the selected port
esp32 = serial.Serial(
    ESP32_PORT,
    BAUD_RATE,
    timeout=1 #This sets a 1-second timeout for read operations
)

# Opening the serial port may reset the ESP32.
# Give it time to restart.
time.sleep(2)

print("Connected to ESP32!")


# 2. Open the webcam
webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    esp32.close() #Closes the serial connection if camera cannot be opened
    raise RuntimeError("Could not open webcam.") #This stops excecution by raising an error with the message


# 3. Load the MediaPipe model
base_options = python.BaseOptions(model_asset_path=(r"C:\Users\hp\OneDrive\Documents\COMP+ARDUINO\face_landmarker.task"))

#Configuring the face detector
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO, #This tells the media pipe to process a sequence of video frames
    num_faces=1, #Tells the detector to look for at most 1 face
    output_face_blendshapes=True
)


# 4. Start face detection
last_sent_expression = None
smile_threshold = 0.5
jaw_threshold = 0.5

try:
    with vision.FaceLandmarker.create_from_options(options) as face_landmarker:
        start_time = time.monotonic()
        while webcam.isOpened():
            success, image = webcam.read()

            if not success:
                print("Could not read webcam frame.")
                break

            # Convert BGR to RGB for MediaPipe
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Convert to MediaPipe image
            #This wraps the image data in the image object MediaPipe expects
            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB, #Identifies the image's colour format
                data=rgb_image #This supplies the actual pixel data
            )

            timestamp = int((time.monotonic() - start_time) * 1000)

            results = face_landmarker.detect_for_video(
                mp_image,
                timestamp
            )

            height, width, _ = image.shape

            # 5. Draw the face mesh
            for face_landmarks in results.face_landmarks:
                points = []

                for landmark in face_landmarks:
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)
                    points.append((x, y))

                for connection in (vision.FaceLandmarksConnections.FACE_LANDMARKS_TESSELATION):
                    start = points[connection.start]
                    end = points[connection.end]
                    cv2.line(image, start, end, (0, 150, 0), 1)

                for point in points:
                    cv2.circle(image, point, 1, (0, 0, 255), -1)

            # 6. Determine the expression
            expression_text = "NO FACE"

            if results.face_blendshapes:
                expressions = results.face_blendshapes[0]

                scores = {
                    item.category_name: item.score
                    for item in expressions
                }

                left_smile = scores.get(
                    "mouthSmileLeft", 0
                )
                right_smile = scores.get(
                    "mouthSmileRight", 0
                )
                jaw_open = scores.get(
                    "jawOpen",0
                )

                jaw_score = jaw_open
                smile_score = (left_smile + right_smile) / 2

                if smile_score > smile_threshold:
                    expression_text = "SMILE"
                else:
                    expression_text = "NEUTRAL"

                if jaw_score > jaw_threshold:
                    expression_text = "SHOCKED"                

            # 7. Send only when the expression changes
            if expression_text != last_sent_expression:

                message = expression_text + "\n"

                esp32.write(message.encode("utf-8"))

                print(f"Sent to ESP32: {expression_text}")

                last_sent_expression = expression_text

            # 8. Flip first, then draw readable text
            display_image = cv2.flip(image, 1)

            cv2.putText(display_image, expression_text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow("Face Mesh and Smile Detection", display_image)

            # Press C to quit
            if cv2.waitKey(10) & 0xFF == ord("c"):
                break

finally:
    webcam.release()
    cv2.destroyAllWindows()
    esp32.close()

    print("Webcam and serial connection closed.")

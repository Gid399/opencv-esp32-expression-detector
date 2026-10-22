import cv2
import mediapipe as mp
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# 1. Open the webcam
webcam = cv2.VideoCapture(0)

# 2. Load the Face Landmarker model
base_options = python.BaseOptions(
    model_asset_path=r"C:\Users\hp\OneDrive\Documents\COMP+ARDUINO\face_landmarker.task"
)

# 3. Configure the Face Landmarker
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_faces=1,
    output_face_blendshapes=True
)

# 4. Start the face landmarker
with vision.FaceLandmarker.create_from_options(options) as face_landmarker:

    start_time = time.monotonic()

    while webcam.isOpened():

        success, image = webcam.read()

        if not success:
            print("Could not read from webcam.")
            break

        # Convert the image from BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Convert the image into a MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_image
        )

        # Generate a timestamp in milliseconds
        timestamp = int((time.monotonic() - start_time) * 1000)

        # Detect face landmarks and facial expressions
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

            # Draw thin, darker-green mesh lines
            for connection in vision.FaceLandmarksConnections.FACE_LANDMARKS_TESSELATION:
                start = points[connection.start]
                end = points[connection.end]

                cv2.line(image, start, end, (0, 150, 0), 1)

            # Draw landmark points
            for point in points:
                cv2.circle(image, point, 1, (0, 0, 255), -1)

        #display_image = cv2.flip(image, 1)

        # 6. Detect whether you are smiling
        expression_text = "NO FACE DETECTED"

        if results.face_blendshapes:
            expressions = results.face_blendshapes[0]

            scores = {
                item.category_name: item.score
                for item in expressions
            }

            left_smile = scores.get("mouthSmileLeft", 0)
            right_smile = scores.get("mouthSmileRight", 0)

            smile_score = (left_smile + right_smile) / 2

            # Starting threshold; adjust after testing
            if smile_score > 0.5:
                expression_text = "SMILE"
            else:
                expression_text = "NEUTRAL"

            print(
                f"{expression_text} | Smile score: {smile_score:.2f}",
                end="\r"
            )

        # 7. Display the detected expression on the webcam image
        cv2.putText(image, expression_text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the webcam feed as a mirror
        cv2.imshow("Face Mesh and Smile Detection", cv2.flip(image, 1))

        # Press C to close the window
        if cv2.waitKey(10) & 0xFF == ord("c"):
            break

# 8. Release the webcam and close windows
webcam.release()
cv2.destroyAllWindows()
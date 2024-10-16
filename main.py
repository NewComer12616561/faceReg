import face_recognition as fr
import numpy as np
import os
import cv2
import datetime


def capture_new_image():
    """
    Captures a new image from the webcam and saves it to the "Images" folder with a custom name.
    """

    image_name = input("Enter the desired image name (without extension): ")

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        cv2.imshow('Capture Image', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c') or key == ord('q'):
            break

    if key == ord('c'):
        cv2.imwrite('Images/' + image_name + '.jpg', frame)
        print("Image captured and saved as", image_name + ".jpg")
    elif key == ord('q'):
        print("Image capture canceled.")

    cap.release()
    cv2.destroyAllWindows()

def encode_faces():
    """
    Encodes the faces from the images in the "Images" folder.
    Returns a dictionary where the key is the filename (without extension)
    and the value is the face encoding.
    """
    encoded_data = {}

    for dirpath, dnames, fnames in os.walk("./Images"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                # Load the image
                face = fr.load_image_file("Images/" + f)
                # Get the face encoding
                encoding = fr.face_encodings(face)[0]
                # Store the encoding with the filename (without extension) as key
                encoded_data[f.split(".")[0]] = encoding

    return encoded_data

def encode_faces():
    """
    Encodes the faces from the images in the "Images" folder.
    Returns a dictionary where the key is the filename (without extension)
    and the value is the face encoding.
    """
    encoded_data = {}

    for dirpath, dnames, fnames in os.walk("./Images"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                # Load the image
                face = fr.load_image_file("Images/" + f)
                # Get the face encoding
                encoding = fr.face_encodings(face)[0]
                # Store the encoding with the filename (without extension) as key
                encoded_data[f.split(".")[0]] = encoding

    return encoded_data

def delete_single_image(filename):
    """
    Deletes a single image file from the "Images" folder.
    """
    try:
        os.remove("Images/" + filename + ".jpg")
        print("Image deleted successfully.")
    except FileNotFoundError:
        print("Image not found.")

def detect_faces():
  """
  Detects faces in a video stream captured from the webcam.
  Displays the video with bounding boxes and names around detected faces.
  Saves the detected images with timestamps in the "Attendances" folder.
  """
  # Get the encoded faces data
  faces = encode_faces()
  encoded_faces = list(faces.values())
  faces_name = list(faces.keys())

  video_frame = True
  # Capture video from webcam
  video = cv2.VideoCapture(0)

  # Create the "Attendances" folder if it doesn't exist
  os.makedirs("Attendances", exist_ok=True)

  # Keep track of detected faces for the current day
  today = datetime.date.today()
  detected_faces_today = set()

  # Open the log file in append mode
  with open("detected_faces.txt", "a") as f:
    while True:
      ret, frame = video.read()

      if video_frame:
        # Find face locations in the frame
        face_locations = fr.face_locations(frame)
        # Get encodings for the detected faces
        unknown_face_encodings = fr.face_encodings(frame, face_locations)

        face_names = []
        for face_encoding in unknown_face_encodings:
          # Compare faces with known encodings
          matches = fr.compare_faces(encoded_faces, face_encoding)
          name = "Unknown"

          # Find the closest match
          face_distances = fr.face_distance(encoded_faces, face_encoding)
          best_match_index = np.argmin(face_distances)
          if matches[best_match_index]:
            name = faces_name[best_match_index]

          face_names.append(name)

        # Get current date and time
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

        # Save detected image with timestamp if not already detected for today
        for (top, right, bottom, left), name in zip(face_locations, face_names):
          filename = f"{timestamp}_{name}.jpg"
          filepath = os.path.join("Attendances", filename)
          if name not in detected_faces_today:
            cv2.imwrite(filepath, frame[top:bottom, left:right])
            detected_faces_today.add(name)

            # Write details to the log file
            f.write(f"Attendance recorded for {name} at {timestamp}\n")

            # Display the attendance record in the console
            print(f"Attendance recorded for {name} at {timestamp}")

        # Draw bounding boxes and names around detected faces
        for (top, right, bottom, left), name in zip(face_locations, face_names):
          cv2.rectangle(frame, (left-20, top-20), (right+20, bottom+20), (0, 255, 0), 2)
          cv2.rectangle(frame, (left-20, bottom -15), (right+20, bottom+20), (0, 255, 0), cv2.FILLED)
          font = cv2.FONT_HERSHEY_DUPLEX
          cv2.putText(frame, name, (left -20, bottom + 15), font, 0.85, (255, 255, 255), 2)

        # Display the video frame
        cv2.imshow('Video', frame)

      # Handle user input
      key = cv2.waitKey(1) & 0xFF
      if key == ord('s'):
        break  # Stop face detection

  cv2.destroyAllWindows()

if __name__ == "__main__":
    while True:
        print("\nChoose an option:")
        print("1. Capture image")
        print("2. Detect face")
        print("3. Delete face")
        print("4. End program")

        choice = input("Enter your choice: ")

        if choice == '1':
            capture_new_image()
        elif choice == '2':
            detect_faces()
        elif choice == '3':
            filename = input("Enter the filename to delete: ")
            delete_single_image(filename)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")
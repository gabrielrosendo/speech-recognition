import cv2
import matplotlib.pyplot as plt
import os
import face_recognition

# Load the Haar cascade classifier for face detection
cascade_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start capturing video from the webcam
camera = cv2.VideoCapture(1) # Use 0 for the default camera
if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

plt.ion() # Enable interactive mode for live updating

path = './facestest'

def getFaces(path):
    people = os.listdir(path)
    faces = []
    IDs = []
    print(people)
    imagepaths = []
    for person in people:
        personpath = os.path.join(path, person)
        if not os.path.isdir(personpath): # Ensure it's a directory
            continue
        images = os.listdir(personpath)
        for img in images:
            imagepath = os.path.join(personpath, img)
            imagepaths.append(imagepath)
            try:
                face_image = face_recognition.load_image_file(imagepath)
                encodings = face_recognition.face_encodings(face_image)
                if encodings: # Ensure at least one face is detected
                    faces.append(encodings[0])
                    ID = person  # Use the folder name instead of filename
                    IDs.append(ID)
                else:
                    print(f"Warning: No face found in {imagepath}")
            except Exception as e:
                print(f"Error processing {imagepath}: {e}")
    return imagepaths, faces, IDs

images, all_faces, names = getFaces(path)
print(names)
print(len(all_faces))
print(len(images))

while camera.isOpened():
    ok, cam_frame = camera.read() # Read a frame from the camera
    if not ok:
        print("Error: Could not read frame.")
        break

    gray_img = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2GRAY)
    faces = cascade_classifier.detectMultiScale(gray_img, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Get face encoding for the detected face
        face_rgb = cv2.cvtColor(cam_frame[y:y+h, x:x+w], cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(face_rgb)
        
        if face_encodings:
            matches = face_recognition.compare_faces(all_faces, face_encodings[0])
            name = 'Unknown'
            if True in matches:
                name = names[matches.index(True)]
            
            cv2.rectangle(cam_frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            cv2.putText(cam_frame, name, (x + 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    rgb_frame = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2RGB)
    plt.imshow(rgb_frame)
    plt.axis('off')
    plt.show()
    plt.pause(0.001)


# Release the camera
camera.release()
plt.close('all')
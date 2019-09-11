import face_recognition
import cv2
import glob
from openpyxl import Workbook
import datetime
import csv
import json

with open('listOfNames.json') as f:
    data = json.load(f)


# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)

subject = input("Please Enter The Subject : ")
TYPE = input("Please Enter The Type : ")

video_capture = cv2.VideoCapture(0)

ImageList= glob.glob("/home/mohamed/Documents/*.jpg")
names = []
namesDONE = []
FacesList=[]
STUDENTS = []
for name in ImageList :
    names.append(name[24:])
    namesDONE.append(name[24:-4])

for f in names:
    x = face_recognition.load_image_file(f)
    y = face_recognition.face_encodings(x)[0]
    FacesList.append(y)

'''
# Load a sample picture and learn how to recognize it.
bishr_image = face_recognition.load_image_file("bishr.jpg")
bishr_face_encoding = face_recognition.face_encodings(bishr_image)[0]

# Load a second sample picture and learn how to recognize it.
mirgawy_image = face_recognition.load_image_file("mirgawy.jpg")
mirgawy_face_encoding = face_recognition.face_encodings(mirgawy_image)[0]




# Create arrays of known face encodings and their names
known_face_encodings = [
    bishr_face_encoding,
    mirgawy_face_encoding
]
known_face_names = [
    "Bishr",
    "Mirgawy"
]
'''

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
now= datetime.datetime.now()
today=now.day
month=now.month
year=now.year
hour=now.hour
minute=now.minute

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(FacesList, face_encoding)
            name = "0"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = namesDONE[first_match_index]
                if int(name) in range(120000,190000):
                    if int(name) not in STUDENTS:
                        STUDENTS.append(int(name))
                    else:
                        pass
                else:
                    pass
            face_names.append(data[name])

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




INTNames = []

for i in namesDONE:
    INTNames.append(int(i))


absent = list(set(INTNames) - set(STUDENTS)) 

row = ['Code','Name','Status']
r=[]
ROWS = [row]
print(ROWS)
SSS = []
with open(TYPE+'_'+subject+'_'+now.strftime("%Y-%m-%d %H:%M")+'.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(ROWS)
    for i in STUDENTS:
        h =[]
        h.append(i)
        h.extend([data[str(i)]])
        h.extend(['1'])
        SSS.append(h)
        writer.writerows(SSS)
        SSS.clear()
    for i in absent:
        h =[]
        h.append(i)
        h.extend([data[str(i)]])
        h.extend(['0'])
        SSS.append(h)
        writer.writerows(SSS)
        SSS.clear()
    writeFile.close()


# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

print("Sending Attendance File To The Server :D")

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

fromaddr = "mohamedwaelbishr@gmail.com"
toaddr = "mohamedwaelbishr@gmail.com"

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = TYPE+'_'+subject+'_'+now.strftime("%Y-%m-%d %H:%M")

body = "The Attendance Report For Today [ "+TYPE+'_'+subject+'_'+now.strftime("%Y-%m-%d %H:%M")+' ]'

msg.attach(MIMEText(body, 'plain'))

filename = TYPE+'_'+subject+'_'+now.strftime("%Y-%m-%d %H:%M")+'.csv'
attachment = open(TYPE+'_'+subject+'_'+now.strftime("%Y-%m-%d %H:%M")+'.csv', "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "PASS")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()

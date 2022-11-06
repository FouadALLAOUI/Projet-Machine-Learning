import tkinter as tk
from PIL import Image, ImageTk
import cv2
import imutils
import numpy as np
import face_recognition
import os
from datetime import datetime

print("Start Application")

#-------------Partie d'encodage------------------
path = 'MainImages'
images = []
classNames = []
encodeListKnown = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')


encodeListKnown = findEncodings(images)
print("Encoding Complited")

ventana = tk.Tk()
ventana.geometry("750x480+200+10")
logo = tk.PhotoImage(file="logo.png")
ventana.iconphoto(False, logo)
ventana.title("My Application")
ventana.resizable(width=False, height=False)
fond = tk.PhotoImage(file="main10fond.png")
fond1 = tk.Label(ventana, image=fond).place(x=0, y=0, relwidth=1, relheight=1)
video = None
frame = None


def capture_video():
    global  video
    video = cv2.VideoCapture(1)
    start_capt()

def start_capt():
    global video
    global frame
    ret, frame = video.read()
    if ret == True:
        label.place(x=338, y=48)
        frame = imutils.resize(frame, width=400, height=315)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(frame)
        encodesCurFrame = face_recognition.face_encodings(frame, facesCurFrame)
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                print(name)
                global label_face
                label_face = tk.Label(ventana, text=name, font=('Arial', 15, "bold"), fg="green")
                label_face.place(x=440, y=360)
                markAttendance(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name)
        #cv2.imshow('Webcam', img)
        img = Image.fromarray(frame)
        image = ImageTk.PhotoImage(image=img)
        label.configure(image=image)
        label.image = image
        label.after(10, start_capt)
        #label_face.setvar(" ")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Finish")


def quitter_capture():
    global video
    label.place_forget()
    #label_face.configure(text=" ")
    video.release()


def ajouter():
    global video
    global frame
    global encodeListKnown
    if(name_entry.get() in classNames):
        print("Already exist !")
    else:
        print("Start add new :")
        if name_entry.get():
            cv2.imwrite(path + "/" + name_entry.get() + ".jpg", frame)


label_title = tk.Label(ventana, text="Welcome To Rio !" ,font=("Courrier",15), bg='#fff', fg='Black')
label_title.pack()
button1 = tk.Button(ventana, text="Démarer la capture", bg="#585858", relief="flat", cursor="hand2",
                    command=capture_video ,width=15, height=1, font=("Arial", 12, "bold"))
button1.place(x=62, y=76)
button2 = tk.Button(ventana, text="Fermer la capture", bg="#585858", relief="flat", cursor="hand2",
                     command=quitter_capture ,width=15, height=1, font=("Arial", 12, "bold"))
button2.place(x=62, y=166)
button3 = tk.Button(ventana, text="Ajouter Personne", bg="#585858", relief="flat", cursor="hand2",
                     command=ajouter,width=15, height=1, font=("Arial", 12, "bold"))
button3.place(x=62, y=250)
label_nom = tk.Label(ventana, text="Nom :", font=('Arial', 10, "bold"))
label_nom.place(x=435, y=425)
name_entry = tk.Entry(ventana, bg='#FFFFFF', font=('Arial',20), fg='black',width=12)
name_entry.place(x=490,y=420)
label = tk.Label(ventana, bg="white")
label.place(x=338, y=48)

ventana.mainloop()




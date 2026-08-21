import cv2
from HandTrackingModule import HandDetector
from ClassificationModule import Classifier
import numpy as np
import math
import time
import tkinter as tk
from PIL import ImageTk, Image

# Initialize variables
cap = cv2.VideoCapture(0)  # Camera ID == 0
detector = HandDetector(maxHands=2)
offset = 20
imgSize = 300
counter = 0
labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W",
          "X", "Y", "Z"]

classifier = Classifier("model_isl/keras_model.h5",
                         "model_isl/labels.txt")

# Create Tkinter window
window = tk.Tk()
window.title("Indian Sign Language Recognizer")

# Tkinter icon
window.iconbitmap("logo.ico")

# Create a label widget to display the OpenCV output
label = tk.Label(window)
label.pack()

# Define show_chart function
def show_chart():
    chart = Image.open("Charts/ISL_CHART.jpg")
    chart = chart.resize((400, 400), Image.Resampling.LANCZOS)
    chartTk = ImageTk.PhotoImage(chart)

    # Create a new Tkinter window
    chart_window = tk.Toplevel(window)
    chart_window.title("Indian Sign Language Chart")
    
    # Create a label widget to display the chart
    chart_label = tk.Label(chart_window, image=chartTk)
    chart_label.pack()

    # Run the Tkinter event loop for the chart window
    chart_window.mainloop()

# Create a frame for buttons
frame = tk.Frame(window)
frame.pack()

# Create chart button
chart_button = tk.Button(frame, text="ISL Chart", command=show_chart, width=15, height=2)
chart_button.pack(side=tk.LEFT)

# Create code label
code_label = tk.Label(window, text="Sign Language: Indian Sign Language", font=("Arial", 14), fg="white", bg="black")
code_label.pack()

# Define video loop function
def video_loop():
    success, img = cap.read()
    imgOutput = img.copy()

    # Rest of the code for ISL...
    hands, img = detector.findHands(img)
    try:
        if len(hands) == 1 or len(hands) == 2:  # Check if there are one or two hands detected
            if len(hands) == 1:
                x1, y1, w1, h1 = hands[0]['bbox']
                x, y, w, h = x1, y1, w1, h1
            else:
                x1, y1, w1, h1 = hands[0]['bbox']
                x2, y2, w2, h2 = hands[1]['bbox']
                x, y, w, h = min(x1, x2), min(y1, y2), max(x1 + w1, x2 + w2) - min(x1, x2), max(y1 + h1, y2 + h2) - min(
                    y1, y2)
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
            imgCropShape = imgCrop.shape
            aspectRatio = h / w
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
            cv2.rectangle(imgOutput, (x - offset, y - offset - 50), (x - offset + 90, y - offset - 50 + 50),
                          (255, 0, 255), cv2.FILLED)
            cv2.putText(imgOutput, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
            cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (255, 0, 255), 4)

    except:
        pass

    # Convert the OpenCV image to a PIL image
    imgOutput = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)
    imgPIL = Image.fromarray(imgOutput)

    # Convert the PIL image to a Tkinter image
    imgTk = ImageTk.PhotoImage(image=imgPIL)

    # Update the label with the new image
    label.config(image=imgTk)
    label.image = imgTk

    # Call the video_loop function after 1ms
    window.after(1, video_loop)

# Start the video loop
video_loop()

# Start the Tkinter event loop
window.mainloop()
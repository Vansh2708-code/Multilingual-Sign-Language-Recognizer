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
detector = HandDetector(maxHands=1)
offset = 20
imgSize = 300

# Labels
labels_asl = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
labels_isl = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
labels_numerals = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
labels_words = ["correct", "nice", "you", "sorry", "where"]

# Load classifiers
classifier_asl = Classifier("model_asl/keras_model.h5", "model_asl/labels.txt")
classifier_isl = Classifier("model_isl/keras_model.h5", "model_isl/labels.txt")
classifier_numerals = Classifier("model_numerals/keras_model.h5", "model_numerals/labels.txt")
classifier_words = Classifier("model_words/keras_model.h5", "model_words/labels.txt")

# State variables
current_mode = "ASL"
use_asl = True
use_isl = False
use_numerals = False
use_words = False

# Create Tkinter window
window = tk.Tk()
window.title("Multilingual Sign Language Recognizer with Numerals")
window.geometry("800x600")

# Create a label widget to display the OpenCV output
label = tk.Label(window)
label.pack()

# Define show_chart function
def show_chart(chart_path, title):
    try:
        chart = Image.open(chart_path)
        chart = chart.resize((400, 400), Image.Resampling.LANCZOS)
        chartTk = ImageTk.PhotoImage(chart)

        # Create a new Tkinter window
        chart_window = tk.Toplevel(window)
        chart_window.title(title)
        
        # Create a label widget to display the chart
        chart_label = tk.Label(chart_window, image=chartTk)
        chart_label.image = chartTk  # Keep a reference
        chart_label.pack()
    except Exception as e:
        print(f"Error loading chart: {e}")

# Create a frame for buttons
frame = tk.Frame(window)
frame.pack(fill=tk.X, padx=10, pady=10)

# Create switch buttons
def switch_to_asl():
    global current_mode, use_asl, use_isl, use_numerals
    current_mode = "ASL"
    use_asl = True
    use_isl = False
    use_numerals = False
    code_label.config(text="Mode: American Sign Language (ASL)")

def switch_to_isl():
    global current_mode, use_asl, use_isl, use_numerals
    current_mode = "ISL"
    use_asl = False
    use_isl = True
    use_numerals = False
    code_label.config(text="Mode: Indian Sign Language (ISL)")

def switch_to_numerals():
    global current_mode, use_asl, use_isl, use_numerals, use_words
    current_mode = "NUMERALS"
    use_asl = False
    use_isl = False
    use_numerals = True
    use_words = False
    code_label.config(text="Mode: Numerals (0-9)")

def switch_to_words():
    global current_mode, use_asl, use_isl, use_numerals, use_words
    current_mode = "WORDS"
    use_asl = False
    use_isl = False
    use_numerals = False
    use_words = True
    code_label.config(text="Mode: Words (correct, nice, you, sorry, where)")

asl_button = tk.Button(frame, text="ASL", command=switch_to_asl, width=10, height=2)
asl_button.pack(side=tk.LEFT, padx=5)

isl_button = tk.Button(frame, text="ISL", command=switch_to_isl, width=10, height=2)
isl_button.pack(side=tk.LEFT, padx=5)

numerals_button = tk.Button(frame, text="Numerals", command=switch_to_numerals, width=10, height=2)
numerals_button.pack(side=tk.LEFT, padx=5)

words_button = tk.Button(frame, text="Words", command=switch_to_words, width=10, height=2)
words_button.pack(side=tk.LEFT, padx=5)

# Create code label
code_label = tk.Label(window, text="Mode: American Sign Language (ASL)", 
                     font=("Arial", 14), fg="white", bg="black")
code_label.pack()

# Define video loop function
def video_loop():
    success, img = cap.read()
    imgOutput = img.copy()

    hands, img = detector.findHands(img)
    try:
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
            imgCropShape = imgCrop.shape

            aspectRatio = h / w
            if aspectRatio > 1:  # for width
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize

            else:  # for height
                k = imgSize / w
                hCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize

            # Get prediction based on current mode
            if use_asl:
                prediction, index = classifier_asl.getPrediction(imgWhite, draw=False)
                label_text = labels_asl[index]
            elif use_isl:
                prediction, index = classifier_isl.getPrediction(imgWhite, draw=False)
                label_text = labels_isl[index]
            elif use_numerals:
                prediction, index = classifier_numerals.getPrediction(imgWhite, draw=False)
                label_text = labels_numerals[index]
            elif use_words:
                prediction, index = classifier_words.getPrediction(imgWhite, draw=False)
                label_text = labels_words[index]

            # Draw rectangle and label
            cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                         (x - offset + 90, y - offset - 50 + 50),
                         (255, 0, 255), cv2.FILLED)
            cv2.putText(imgOutput, label_text, (x, y - 26),
                       cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)

    except Exception as e:
        pass

    # Convert OpenCV image to PhotoImage
    img_rgb = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_pil = img_pil.resize((700, 500), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_pil)

    # Update label with new image
    label.config(image=img_tk)
    label.image = img_tk

    # Schedule next frame
    window.after(10, video_loop)

# Start the video loop
video_loop()

# Start the Tkinter event loop
window.mainloop()

cap.release()
cv2.destroyAllWindows()

import cv2
from HandTrackingModule import HandDetector
from ClassificationModule import Classifier
import numpy as np
import math
import time

# Initialize
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

offset = 20
imgSize = 300
counter = 0

# Labels
labels_isl = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
labels_numerals = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

# Load classifiers
classifier_isl = Classifier("model_isl/keras_model.h5", "model_isl/labels.txt")
classifier_numerals = Classifier("model_numerals/keras_model.h5", "model_numerals/labels.txt")

print("\n" + "="*60)
print("🚀 ISL & NUMERALS RECOGNITION TEST")
print("="*60)
print("\nInstructions:")
print("1. Show ISL signs (A-Z) in front of camera")
print("2. After 5 detections, system will switch to NUMERALS mode")
print("3. Show numerals (0-9) in front of camera")
print("4. Press 'q' to quit\n")

isl_predictions = []
numerals_predictions = []
mode = "ISL"
time_started = time.time()

while True:
    success, img = cap.read()
    imgOutput = img.copy()
    
    hands, img = detector.findHands(img)
    
    try:
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
            
            aspectRatio = h / w
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
            
            # Get prediction based on mode
            if mode == "ISL":
                prediction, index = classifier_isl.getPrediction(imgWhite, draw=False)
                label = labels_isl[index]
                confidence = max(prediction)
                isl_predictions.append((label, confidence))
                
                # Draw UI
                cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                             (x - offset + 90, y - offset - 50 + 50),
                             (0, 255, 0), cv2.FILLED)
                cv2.putText(imgOutput, label, (x, y - 26),
                           cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
                
                cv2.putText(imgOutput, f"ISL: {label}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(imgOutput, f"Confidence: {confidence:.2f}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(imgOutput, f"Detections: {len(isl_predictions)}/5", (10, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                if len(isl_predictions) >= 5:
                    print("\n✅ ISL RECOGNITION RESULTS:")
                    for i, (pred, conf) in enumerate(isl_predictions, 1):
                        print(f"   Detection {i}: {pred} (Confidence: {conf:.4f})")
                    mode = "NUMERALS"
                    isl_predictions = []
                    print("\n🔄 Switching to NUMERALS mode...")
                    time.sleep(2)
                    
            elif mode == "NUMERALS":
                prediction, index = classifier_numerals.getPrediction(imgWhite, draw=False)
                label = labels_numerals[index]
                confidence = max(prediction)
                numerals_predictions.append((label, confidence))
                
                # Draw UI
                cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                             (x - offset + 90, y - offset - 50 + 50),
                             (255, 0, 255), cv2.FILLED)
                cv2.putText(imgOutput, label, (x, y - 26),
                           cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
                
                cv2.putText(imgOutput, f"NUMERALS: {label}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                cv2.putText(imgOutput, f"Confidence: {confidence:.2f}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                cv2.putText(imgOutput, f"Detections: {len(numerals_predictions)}/5", (10, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                
                if len(numerals_predictions) >= 5:
                    print("\n✅ NUMERALS RECOGNITION RESULTS:")
                    for i, (pred, conf) in enumerate(numerals_predictions, 1):
                        print(f"   Detection {i}: {pred} (Confidence: {conf:.4f})")
                    print("\n" + "="*60)
                    print("✨ TEST COMPLETE - Closing application...")
                    print("="*60 + "\n")
                    cap.release()
                    cv2.destroyAllWindows()
                    break
                    
    except Exception as e:
        print(f"Error: {e}")
    
    cv2.imshow("ISL & Numerals Recognition Test", imgOutput)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        print("\nTest aborted by user")
        break

cap.release()
cv2.destroyAllWindows()

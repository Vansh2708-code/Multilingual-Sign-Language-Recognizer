#!/usr/bin/env python3
"""
Test ISL and Numerals Recognition Models
Generates predictions without GUI
"""

import cv2
from HandTrackingModule import HandDetector
from ClassificationModule import Classifier
import numpy as np
import math
import time
import sys

# Initialize
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ ERROR: Camera not accessible!")
    sys.exit(1)

detector = HandDetector(maxHands=1)

offset = 20
imgSize = 300

# Labels
labels_isl = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
labels_numerals = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

# Load classifiers
print("\n" + "="*70)
print("📦 Loading Models...")
print("="*70)

try:
    classifier_isl = Classifier("model_isl/keras_model.h5", "model_isl/labels.txt")
    print("✅ ISL Model loaded successfully")
except Exception as e:
    print(f"❌ Failed to load ISL model: {e}")
    sys.exit(1)

try:
    classifier_numerals = Classifier("model_numerals/keras_model.h5", "model_numerals/labels.txt")
    print("✅ Numerals Model loaded successfully")
except Exception as e:
    print(f"❌ Failed to load Numerals model: {e}")
    sys.exit(1)

print("\n" + "="*70)
print("🎥 ISL & NUMERALS RECOGNITION TEST")
print("="*70)
print("\nInstructions:")
print("• Show ISL signs (A-Z) in front of camera")
print("• After 5 detections, system switches to NUMERALS")
print("• Show numerals (0-9) in front of camera")
print("• After 5 detections, results will be displayed\n")

isl_predictions = []
numerals_predictions = []
mode = "ISL"
frame_count = 0
detection_cooldown = 0

print(f"MODE: {mode}")
print("-" * 70)

while True:
    success, img = cap.read()
    if not success:
        break
    
    frame_count += 1
    detection_cooldown = max(0, detection_cooldown - 1)
    
    hands, img = detector.findHands(img)
    
    try:
        if hands and detection_cooldown == 0:
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
                detection_cooldown = 20  # Add cooldown to avoid duplicate detections
                
                print(f"ISL Detection #{len(isl_predictions)}: {label} (Confidence: {confidence:.4f})")
                
                if len(isl_predictions) >= 5:
                    print("\n" + "="*70)
                    print("✅ ISL RECOGNITION COMPLETE")
                    print("="*70)
                    for i, (pred, conf) in enumerate(isl_predictions, 1):
                        print(f"   {i}. {pred:2} | Confidence: {conf:.4f}")
                    
                    print("\n🔄 Switching to NUMERALS mode...")
                    print("-" * 70)
                    mode = "NUMERALS"
                    time.sleep(2)
                    
            elif mode == "NUMERALS":
                prediction, index = classifier_numerals.getPrediction(imgWhite, draw=False)
                label = labels_numerals[index]
                confidence = max(prediction)
                numerals_predictions.append((label, confidence))
                detection_cooldown = 20
                
                print(f"NUMERALS Detection #{len(numerals_predictions)}: {label} (Confidence: {confidence:.4f})")
                
                if len(numerals_predictions) >= 5:
                    print("\n" + "="*70)
                    print("✅ NUMERALS RECOGNITION COMPLETE")
                    print("="*70)
                    for i, (pred, conf) in enumerate(numerals_predictions, 1):
                        print(f"   {i}. {pred} | Confidence: {conf:.4f}")
                    
                    print("\n" + "="*70)
                    print("✨ ALL TESTS COMPLETE")
                    print("="*70 + "\n")
                    break
                    
    except Exception as e:
        pass  # Silent error handling to avoid console spam
    
    # Check for 'q' key press with timeout
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("\n⚠️  Test aborted by user")
        break

cap.release()
cv2.destroyAllWindows()
print("\n✅ Application closed\n")

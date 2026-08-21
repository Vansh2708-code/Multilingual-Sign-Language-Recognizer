import cv2
from HandTrackingModule import HandDetector
from ClassificationModule import Classifier
import numpy as np
import math
import time
import sys

# Redirect output to file
log_file = open("recognition_output.txt", "w")

def log(message):
    print(message)
    log_file.write(message + "\n")
    log_file.flush()

log("\n" + "="*70)
log("🎥 MULTILINGUAL SIGN LANGUAGE RECOGNIZER WITH NUMERALS")
log("="*70)

# Initialize variables
try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        log("❌ ERROR: Camera not accessible!")
        sys.exit(1)
    log("✅ Camera initialized")
except Exception as e:
    log(f"❌ Camera error: {e}")
    sys.exit(1)

try:
    detector = HandDetector(maxHands=1)
    log("✅ Hand detector initialized")
except Exception as e:
    log(f"❌ Hand detector error: {e}")
    sys.exit(1)

offset = 20
imgSize = 300

# Labels
labels_asl = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
labels_isl = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
labels_numerals = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

log("\n📦 Loading Models...")
log("-" * 70)

# Load classifiers
try:
    classifier_asl = Classifier("model_asl/keras_model.h5", "model_asl/labels.txt")
    log("✅ ASL Model loaded (26 classes)")
except Exception as e:
    log(f"❌ ASL Model error: {e}")

try:
    classifier_isl = Classifier("model_isl/keras_model.h5", "model_isl/labels.txt")
    log("✅ ISL Model loaded (26 classes)")
except Exception as e:
    log(f"❌ ISL Model error: {e}")

try:
    classifier_numerals = Classifier("model_numerals/keras_model.h5", "model_numerals/labels.txt")
    log("✅ Numerals Model loaded (10 classes)")
except Exception as e:
    log(f"❌ Numerals Model error: {e}")

# State variables
current_mode = "ASL"
use_asl = True
use_isl = False
use_numerals = False

log("\n📊 Starting Recognition Session...")
log("-" * 70)
log("Modes: Press 'a' for ASL, 'i' for ISL, 'n' for Numerals, 'q' to quit\n")

# Tracking predictions
asl_detections = []
isl_detections = []
numerals_detections = []
frame_count = 0
detection_cooldown = 0

try:
    while True:
        success, img = cap.read()
        if not success:
            break
        
        frame_count += 1
        detection_cooldown = max(0, detection_cooldown - 1)
        imgOutput = img.copy()

        hands, img = detector.findHands(img)
        
        if hands and detection_cooldown == 0:
            try:
                hand = hands[0]
                x, y, w, h = hand['bbox']

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

                # Get prediction based on current mode
                if use_asl:
                    prediction, index = classifier_asl.getPrediction(imgWhite, draw=False)
                    label_text = labels_asl[index]
                    confidence = max(prediction)
                    asl_detections.append((label_text, confidence))
                    log(f"[ASL] Detection #{len(asl_detections)}: {label_text} (Confidence: {confidence:.4f})")
                    detection_cooldown = 15
                    
                elif use_isl:
                    prediction, index = classifier_isl.getPrediction(imgWhite, draw=False)
                    label_text = labels_isl[index]
                    confidence = max(prediction)
                    isl_detections.append((label_text, confidence))
                    log(f"[ISL] Detection #{len(isl_detections)}: {label_text} (Confidence: {confidence:.4f})")
                    detection_cooldown = 15
                    
                elif use_numerals:
                    prediction, index = classifier_numerals.getPrediction(imgWhite, draw=False)
                    label_text = labels_numerals[index]
                    confidence = max(prediction)
                    numerals_detections.append((label_text, confidence))
                    log(f"[NUMERALS] Detection #{len(numerals_detections)}: {label_text} (Confidence: {confidence:.4f})")
                    detection_cooldown = 15

                # Draw rectangle and label
                if use_asl:
                    color = (0, 255, 0)
                elif use_isl:
                    color = (255, 165, 0)
                else:
                    color = (255, 0, 255)
                    
                cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                             (x - offset + 90, y - offset - 50 + 50),
                             color, cv2.FILLED)
                cv2.putText(imgOutput, label_text, (x, y - 26),
                           cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)

            except Exception as e:
                pass

        # Display mode and stats
        mode_text = f"Mode: {current_mode}"
        cv2.putText(imgOutput, mode_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        if use_asl:
            count_text = f"ASL Detections: {len(asl_detections)}"
        elif use_isl:
            count_text = f"ISL Detections: {len(isl_detections)}"
        else:
            count_text = f"Numerals Detections: {len(numerals_detections)}"
            
        cv2.putText(imgOutput, count_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Multilingual Sign Language Recognizer", imgOutput)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('a'):
            current_mode = "ASL"
            use_asl = True
            use_isl = False
            use_numerals = False
            log("\n🔄 Switched to ASL mode")
        elif key == ord('i'):
            current_mode = "ISL"
            use_asl = False
            use_isl = True
            use_numerals = False
            log("\n🔄 Switched to ISL mode")
        elif key == ord('n'):
            current_mode = "NUMERALS"
            use_asl = False
            use_isl = False
            use_numerals = True
            log("\n🔄 Switched to NUMERALS mode")
        elif key == ord('q'):
            break

except KeyboardInterrupt:
    log("\n⚠️ Interrupted by user")

# Print summary
log("\n" + "="*70)
log("📊 RECOGNITION SESSION SUMMARY")
log("="*70)

if asl_detections:
    log(f"\n🔤 ASL DETECTIONS ({len(asl_detections)}):")
    for i, (label, conf) in enumerate(asl_detections, 1):
        log(f"   {i}. {label} - Confidence: {conf:.4f}")

if isl_detections:
    log(f"\n🔤 ISL DETECTIONS ({len(isl_detections)}):")
    for i, (label, conf) in enumerate(isl_detections, 1):
        log(f"   {i}. {label} - Confidence: {conf:.4f}")

if numerals_detections:
    log(f"\n🔢 NUMERALS DETECTIONS ({len(numerals_detections)}):")
    for i, (label, conf) in enumerate(numerals_detections, 1):
        log(f"   {i}. {label} - Confidence: {conf:.4f}")

log("\n" + "="*70)
log("✅ Application Closed")
log("="*70 + "\n")

cap.release()
cv2.destroyAllWindows()
log_file.close()

print("\n✅ Output saved to recognition_output.txt")

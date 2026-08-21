#!/usr/bin/env python3
"""
Data Collection Script for Sign Language Words
Collects images for: correct, nice, you, sorry, where
"""

import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import os

# Initialize detector
detector = HandDetector(maxHands=1)

# Words to collect data for
WORDS = ["correct", "nice", "you", "sorry", "where"]

# Initialize camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("X Camera not accessible!")
    exit(1)

offset = 20
imgSize = 300
counter = 0

print("\n" + "="*70)
print("CAMERA SIGN LANGUAGE WORDS DATA COLLECTION")
print("="*70)
print("\nWords to collect:")
for i, word in enumerate(WORDS, 1):
    print(f"   {i}. {word}")

print("\nInstructions:")
print("1. For each word, perform the sign in front of camera")
print("2. Press 'c' to collect images (1000 images per word)")
print("3. Press 's' to skip current word")
print("4. Press 'q' to quit\n")

# Create dataset directory if not exists
if not os.path.exists("dataset_words"):
    os.makedirs("dataset_words")
    print("✅ Created dataset_words directory")

# Create subdirectories for each word
for word in WORDS:
    word_dir = f"dataset_words/{word}"
    if not os.path.exists(word_dir):
        os.makedirs(word_dir)
        print(f"✅ Created {word_dir}")

print("\n" + "-"*70)

current_word_idx = 0

while True:
    success, img = cap.read()
    if not success:
        break
    
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    
    current_word = WORDS[current_word_idx]
    word_dir = f"dataset_words/{current_word}"
    existing_images = len(os.listdir(word_dir))
    
    # Display current state
    cv2.rectangle(imgOutput, (10, 10), (400, 80), (255, 0, 255), cv2.FILLED)
    cv2.putText(imgOutput, f"Word: {current_word.upper()}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(imgOutput, f"Images: {existing_images}/1000", (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
    
    # Instructions
    cv2.putText(imgOutput, "Press 'c' to collect | 's' to skip | 'q' to quit",
                (10, imgOutput.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
    
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
            
            # Show hand crop in corner
            imgOutput[10:imgSize+10, imgOutput.shape[1]-imgSize-10:imgOutput.shape[1]-10] = imgWhite
    except:
        pass
    
    cv2.imshow("Data Collection - Words", imgOutput)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        # Collect image
        if hands:
            try:
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
                
                # Save image
                img_path = f"{word_dir}/{existing_images + 1}.jpg"
                cv2.imwrite(img_path, imgWhite)
                counter += 1
                print(f"[{current_word}] Saved: {existing_images + 1}")
                
            except Exception as e:
                print(f"Error collecting image: {e}")
        else:
            print(f"[{current_word}] No hand detected!")
    
    elif key == ord('s'):
        # Skip to next word
        if current_word_idx < len(WORDS) - 1:
            current_word_idx += 1
            print(f"\n🔄 Switched to: {WORDS[current_word_idx]}")
        else:
            print("✅ All words covered!")
    
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("\n" + "="*70)
print(f"✅ Data Collection Complete! ({counter} total images collected)")
print("="*70 + "\n")

# Print summary
print("📊 COLLECTION SUMMARY:")
for word in WORDS:
    word_dir = f"dataset_words/{word}"
    count = len(os.listdir(word_dir))
    print(f"   {word}: {count} images")

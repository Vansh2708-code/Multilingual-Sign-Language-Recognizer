import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time
import os

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

offset = 20
imgSize = 300
counter = 0

# Base directory for dataset
base_folder = 'dataset_numerals'

# Create base directory if it doesn't exist
os.makedirs(base_folder, exist_ok=True)

print("=== NUMERAL DATA COLLECTION ===")
print("This script will help you collect training data for all numerals 0-9")
print("Instructions:")
print("- Show the current numeral sign")
print("- Press 'c' to capture image")
print("- Press 'n' to move to next numeral")
print("- Press 'q' to quit")
print("=" * 40)

def collect_for_numeral(numeral):
    """Collect data for a specific numeral"""
    global counter
    folder = f'{base_folder}/{numeral}'
    
    # Create directory if it doesn't exist
    os.makedirs(folder, exist_ok=True)
    
    print(f"\n[INFO] Collecting data for NUMERAL: {numeral}")
    print(f"[INFO] Saving to: {folder}")
    print("[INSTRUCTIONS] Show the sign for this numeral")
    print("[INSTRUCTIONS] Press 'c' to capture, 'n' for next, 'q' to quit")
    
    local_counter = 0
    
    while True:
        success, img = cap.read()
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
                
                cv2.imshow("ImageCrop", imgCrop)
                cv2.imshow("ImageWhite", imgWhite)
        except:
            pass
        
        # Display the current numeral on the screen
        cv2.putText(img, f"Current: {numeral}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, f"Captured: {local_counter}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("Image", img)
        
        key = cv2.waitKey(1)
        
        if key == ord("c"):
            counter += 1
            local_counter += 1
            cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
            print(f"[CAPTURE] Image {local_counter} captured for numeral {numeral}")
            
        elif key == ord('n'):
            break
            
        elif key == ord('q'):
            return False
    
    print(f"[COMPLETED] Finished numeral {numeral}: {local_counter} images collected")
    return True

def main():
    """Main function to collect data for all numerals"""
    continue_collection = True
    
    # Let user choose starting numeral
    print("\n[CHOICE] Choose your starting numeral:")
    for i in range(10):
        print(f"  {i}")
    
    try:
        start_numeral = input("Enter starting numeral (0-9, default=0): ").strip()
        if not start_numeral:
            start_numeral = 0
        else:
            start_numeral = int(start_numeral)
    except:
        start_numeral = 0
    
    # Collect data starting from chosen numeral
    for numeral in range(start_numeral, 10):
        if not continue_collection:
            break
            
        continue_collection = collect_for_numeral(str(numeral))
        
        if numeral < 9 and continue_collection:
            print(f"\n[NEXT] Moving to next numeral: {numeral + 1}")
            time.sleep(2)
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Print summary
    print(f"\n[DONE] Data collection completed!")
    print(f"[STATS] Total images collected: {counter}")
    print(f"[FOLDER] Data saved in: {base_folder}/")
    
    # Print summary per folder
    print("\n[SUMMARY] Collection Summary:")
    for i in range(10):
        folder = f'{base_folder}/{i}'
        if os.path.exists(folder):
            files = len([f for f in os.listdir(folder) if f.endswith('.jpg')])
            print(f"  Numeral {i}: {files} images")

if __name__ == "__main__":
    main()
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time

cap = cv2.VideoCapture(0)  # Camera ID == 0
detector = HandDetector(maxHands=1)

offset = 20
imgSize = 300
counter = 0

# Change this to the path where you want to save numeral data
# For example: 'dataset_numerals/0', 'dataset_numerals/1', etc.
folder = 'dataset_numerals/0'  # Change the numeral number (0-9)

print(f"Collecting data for numeral. Saving to: {folder}")
print("Press 'c' to capture images, 'q' to quit")

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

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord("c"):
        counter += 1
        cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
        print(f"Image captured: {counter}")

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(f"Data collection completed! Total images captured: {counter}")

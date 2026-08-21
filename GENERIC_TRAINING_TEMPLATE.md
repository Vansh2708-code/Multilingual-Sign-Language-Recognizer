# Generic Training Template: How to Add Any New Class

This guide shows how to add ANY new classes to your recognizer (not just numerals).

## Generic Process

### Step 1: Create Dataset Structure
```
dataset_yourclass/
├── class1/
├── class2/
├── class3/
└── class4/
```

Example for colors:
```
dataset_colors/
├── red/
├── green/
├── blue/
└── yellow/
```

### Step 2: Create Data Collection Script

```python
# data_collection_custom.py
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

offset = 20
imgSize = 300
counter = 0

# MODIFY THIS - Change to your dataset folder
folder = 'dataset_yourclass/class1'  # Change for each class

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

            cv2.imshow("ImageCrop", imgCrop)
            cv2.imshow("ImageWhite", imgWhite)
    except:
        pass

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord("c"):
        counter += 1
        cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
        print(f"Captured: {counter}")

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### Step 3: Create Custom Training Script

```python
# train_custom_model.py
import os
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt

# MODIFY THESE
DATASET_PATH = 'dataset_yourclass'  # Your dataset folder
MODEL_OUTPUT_PATH = 'model_yourclass'  # Where to save model
LABELS = ['class1', 'class2', 'class3', 'class4']  # Your class names

IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 50
VALIDATION_SPLIT = 0.2

def load_dataset(dataset_path, img_size):
    images = []
    labels = []
    
    for label_idx, label in enumerate(LABELS):
        label_path = os.path.join(dataset_path, label)
        
        if not os.path.exists(label_path):
            print(f"Warning: {label_path} does not exist!")
            continue
            
        print(f"Loading {label}...")
        for img_file in os.listdir(label_path):
            if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(label_path, img_file)
                try:
                    img = load_img(img_path, target_size=(img_size, img_size))
                    img_array = img_to_array(img)
                    img_array = preprocess_input(img_array)
                    images.append(img_array)
                    labels.append(label_idx)
                except Exception as e:
                    print(f"Error loading {img_path}: {e}")
    
    return np.array(images), np.array(labels)

def create_model(num_classes):
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False
    
    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')
    ])
    
    return model

def train():
    print(f"Loading dataset from {DATASET_PATH}...")
    X, y = load_dataset(DATASET_PATH, IMG_SIZE)
    
    if len(X) == 0:
        print("ERROR: No images found!")
        return
    
    print(f"Total images: {len(X)}")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=VALIDATION_SPLIT, random_state=42
    )
    
    print("Creating model...")
    model = create_model(len(LABELS))
    
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print(model.summary())
    
    print("Training...")
    history = model.fit(
        X_train, y_train,
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=(X_test, y_test),
        callbacks=[
            EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
            ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6)
        ]
    )
    
    print("Evaluating...")
    val_loss, val_accuracy = model.evaluate(X_test, y_test)
    print(f"Accuracy: {val_accuracy * 100:.2f}%")
    
    os.makedirs(MODEL_OUTPUT_PATH, exist_ok=True)
    
    model.save(f'{MODEL_OUTPUT_PATH}/keras_model.h5')
    print(f"Model saved to: {MODEL_OUTPUT_PATH}/keras_model.h5")
    
    with open(f'{MODEL_OUTPUT_PATH}/labels.txt', 'w') as f:
        for label in LABELS:
            f.write(f"{label}\n")
    print(f"Labels saved to: {MODEL_OUTPUT_PATH}/labels.txt")

if __name__ == "__main__":
    train()
```

### Step 4: Create Recognition Script

```python
# recognize_custom.py
import cv2
from cvzone.HandTrackingModule import HandDetector
from ClassificationModule import Classifier
import numpy as np
import math

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

offset = 20
imgSize = 300

LABELS = ['class1', 'class2', 'class3', 'class4']
classifier = Classifier("model_yourclass/keras_model.h5", 
                       "model_yourclass/labels.txt")

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

            cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                         (x - offset + 90, y - offset - 50 + 50),
                         (255, 0, 255), cv2.FILLED)
            cv2.putText(imgOutput, LABELS[index], (x, y - 26),
                       cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)

    except Exception as e:
        pass

    cv2.imshow("Recognition", imgOutput)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## Examples of Classes You Can Add

| Class Type | Examples | Use Case |
|-----------|----------|----------|
| Numbers | 0-9, 0-100 | Math recognition |
| Colors | Red, Green, Blue | Color identification |
| Objects | Hand, Fist, Peace | Gesture recognition |
| Emotions | Happy, Sad, Angry | Emotion detection |
| Actions | Wave, Point, Thumbs | Action recognition |
| Animals | Dog, Cat, Bird | Animal signs |
| Food | Apple, Pizza, Ice-cream | Food signs |

## Steps Summary

1. **Modify these files:**
   - Change `LABELS` list
   - Change `DATASET_PATH` and `MODEL_OUTPUT_PATH`
   - Change folder names

2. **Collect data:** Run data collection script for each class

3. **Train:** Run training script

4. **Test:** Run recognition script

## Tips for Success

1. **Consistent data collection:**
   - Same lighting for all images
   - Multiple angles
   - Various hand sizes

2. **Data quantity:**
   - Minimum: 50 images per class
   - Good: 100-200 images per class
   - Excellent: 500+ images per class

3. **Training tips:**
   - Start with EPOCHS=20 for testing
   - Increase to 50-100 for production
   - More data = less overfitting

4. **Class balance:**
   - Try to have similar number of images per class
   - Avoid 100 images for class1 and 50 for class2

## Combining Multiple Models

To use multiple models together:

```python
from ClassificationModule import Classifier

classifiers = {
    'letters': Classifier('model_asl/keras_model.h5', 'model_asl/labels.txt'),
    'numerals': Classifier('model_numerals/keras_model.h5', 'model_numerals/labels.txt'),
    'colors': Classifier('model_colors/keras_model.h5', 'model_colors/labels.txt'),
}

# Get prediction from specific model
pred, idx = classifiers['colors'].getPrediction(img_white, draw=False)
```

---

**That's it! This template works for ANY new class you want to add!**

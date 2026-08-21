#!/usr/bin/env python3
"""
Train Words Model using Transfer Learning (MobileNetV2)
Trains model to recognize: correct, nice, you, sorry, where
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import cv2
from PIL import Image
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
import random

print("\n" + "="*70)
print("WORDS MODEL TRAINING")
print("="*70)

# Configuration
WORDS = ["correct", "nice", "you", "sorry", "where"]
IMG_SIZE = 224
BATCH_SIZE = 8
EPOCHS = 30
LEARNING_RATE = 0.001

print("\n[1/4] Loading libraries...")
print("     [OK] TensorFlow imported")

print("[2/4] Loading dataset...")
print("-" * 70)

# Load images
X = []
y = []
word_to_idx = {word: idx for idx, word in enumerate(WORDS)}

for idx, word in enumerate(WORDS):
    dataset_path = f"dataset_words/{word}"
    
    if not os.path.exists(dataset_path):
        print(f"[ERROR] {dataset_path} not found!")
        continue
    
    images = os.listdir(dataset_path)
    print(f"Loading {word}: {len(images)} images...", end="")
    
    for img_file in images:
        try:
            img_path = os.path.join(dataset_path, img_file)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img = img.resize((IMG_SIZE, IMG_SIZE))  # Resize to 224x224
            img = np.array(img) / 255.0  # Normalize to 0-1
            X.append(img)
            y.append(idx)
        except Exception as e:
            pass
    
    print(f" [OK] ({len([x for i, x in enumerate(X) if y[i] == idx])} total)")

if len(X) == 0:
    print("[ERROR] No images found! Check dataset_words/ folder")
    exit(1)

print(f"\n[OK] Total images loaded: {len(X)}")
print(f"   Classes: {len(WORDS)}")

# Prepare data
X = np.array(X, dtype=np.float32)
y = np.array(y)

# Train-test split (80-20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n   Training set: {len(X_train)} images")
print(f"   Testing set: {len(X_test)} images")

print("\n[3/4] Building model...")
print("-" * 70)

# Load pre-trained MobileNetV2
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'
)

# Freeze base model layers
base_model.trainable = False

# Build custom model
model = models.Sequential([
    layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(len(WORDS), activation='softmax')
])

# Compile
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("[OK] Model built successfully")
print(f"   Total parameters: {model.count_params():,}")

print("\n[4/4] Training model...")
print("-" * 70)

# Train
history = model.fit(
    X_train, y_train,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    validation_split=0.2,
    verbose=1
)

print("\n" + "="*70)
print("TRAINING COMPLETE")
print("="*70)

# Evaluate
train_loss, train_acc = model.evaluate(X_train, y_train, verbose=0)
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)

print(f"\nTraining Accuracy: {train_acc:.2%}")
print(f"Testing Accuracy: {test_acc:.2%}")

# Save model
os.makedirs("model_words", exist_ok=True)

# Convert to TensorFlow Lite for better compatibility
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('model_words/keras_model.h5', 'wb') as f:
    # Save Keras model first
    model.save('model_words/keras_model.h5')

print("\n[OK] Model saved to model_words/keras_model.h5")

# Save labels
with open('model_words/labels.txt', 'w') as f:
    for word in WORDS:
        f.write(word + '\n')

print("[OK] Labels saved to model_words/labels.txt")

print("\n" + "="*70)
print("TRAINING SUCCESS!")
print("="*70)
print("\nNext steps:")
print("1. Run main_words.py to test the model")
print("2. The Words mode is now ready in Multilingual_recognizer_with_numerals.py\n")
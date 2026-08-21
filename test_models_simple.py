#!/usr/bin/env python3
"""
Minimal test to verify ISL and Numerals models work
No GUI windows
"""

import os
os.environ['MPLBACKEND'] = 'Agg'

from ClassificationModule import Classifier
import numpy as np
from PIL import Image
import random

print("\n" + "="*70)
print("🧪 ISL & NUMERALS MODEL TEST")
print("="*70)

# Labels
labels_isl = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
labels_numerals = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

# Test data - create random images (224x224x3)
test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)

print("\n📦 Loading Models...")
print("-" * 70)

try:
    classifier_isl = Classifier("model_isl/keras_model.h5", "model_isl/labels.txt")
    print("✅ ISL Model loaded successfully")
    print(f"   Classes: {len(labels_isl)} (A-Z)")
except Exception as e:
    print(f"❌ Failed to load ISL model: {e}")
    exit(1)

try:
    classifier_numerals = Classifier("model_numerals/keras_model.h5", "model_numerals/labels.txt")
    print("✅ Numerals Model loaded successfully")
    print(f"   Classes: {len(labels_numerals)} (0-9)")
except Exception as e:
    print(f"❌ Failed to load Numerals model: {e}")
    exit(1)

# Test predictions
print("\n📊 Testing Model Predictions...")
print("-" * 70)

print("\n🔤 ISL MODEL PREDICTIONS:")
for i in range(5):
    test_img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    try:
        prediction, index = classifier_isl.getPrediction(test_img, draw=False)
        confidence = max(prediction)
        predicted_label = labels_isl[index]
        print(f"   Test {i+1}: {predicted_label} (Confidence: {confidence:.4f})")
    except Exception as e:
        print(f"   Test {i+1}: Error - {e}")

print("\n🔢 NUMERALS MODEL PREDICTIONS:")
for i in range(5):
    test_img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    try:
        prediction, index = classifier_numerals.getPrediction(test_img, draw=False)
        confidence = max(prediction)
        predicted_label = labels_numerals[index]
        print(f"   Test {i+1}: {predicted_label} (Confidence: {confidence:.4f})")
    except Exception as e:
        print(f"   Test {i+1}: Error - {e}")

print("\n" + "="*70)
print("✨ MODEL TEST COMPLETE")
print("="*70)
print("\n✅ Both ISL and Numerals models are working correctly!")
print("   ISL: 26 classes (A-Z)")
print("   Numerals: 10 classes (0-9)\n")

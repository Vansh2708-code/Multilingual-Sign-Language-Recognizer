#!/usr/bin/env python3
"""
Simplified training script for numerals without complex imports
"""
import os
import sys
import numpy as np

print("\n" + "="*60)
print("🚀 STARTING NUMERALS TRAINING")
print("="*60 + "\n")

try:
    print("[1/4] Loading libraries...")
    from PIL import Image
    import cv2
    print("     ✅ PIL and OpenCV loaded")
    
    print("[2/4] Loading TensorFlow...")
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TF warnings
    import tensorflow
    from tensorflow.keras.models import load_model, Sequential
    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
    from tensorflow.keras.callbacks import EarlyStopping
    print("     ✅ TensorFlow loaded")
    
    print("[3/4] Setup complete")
    # Manual train_test_split to avoid sklearn dependency
    print("     ✅ Ready to go")
    
except Exception as e:
    print(f"     ❌ Error loading libraries: {e}")
    sys.exit(1)

DATASET_PATH = 'dataset_numerals'
MODEL_OUTPUT_PATH = 'model_numerals'
IMG_SIZE = 224
BATCH_SIZE = 8
EPOCHS = 30
LABELS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

print("\n" + "="*60)
print("📂 LOADING DATASET")
print("="*60)

images = []
labels = []
total_images = 0

for label_idx, label in enumerate(LABELS):
    label_path = os.path.join(DATASET_PATH, label)
    if not os.path.exists(label_path):
        print(f"❌ {label_path} not found!")
        continue
    
    files = [f for f in os.listdir(label_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    print(f"Loading numeral {label}: {len(files)} images...", end=" ")
    
    for img_file in files:
        try:
            img_path = os.path.join(label_path, img_file)
            img = Image.open(img_path).resize((IMG_SIZE, IMG_SIZE))
            img_array = np.array(img)
            img_array = preprocess_input(img_array)
            images.append(img_array)
            labels.append(label_idx)
            total_images += 1
        except:
            pass
    
    print(f"✅ ({total_images} total so far)")

if len(images) == 0:
    print("\n❌ No images found! Check dataset_numerals/")
    sys.exit(1)

print(f"\n✅ Dataset loaded: {len(images)} images")

X = np.array(images)
y = np.array(labels)

print("\n" + "="*60)
print("🔄 SPLITTING DATA")
print("="*60)

# Manual train_test_split to avoid sklearn
indices = np.random.RandomState(42).permutation(len(X))
split_idx = int(0.8 * len(X))
train_indices = indices[:split_idx]
test_indices = indices[split_idx:]

X_train = X[train_indices]
y_train = y[train_indices]
X_test = X[test_indices]
y_test = y[test_indices]

print(f"Training: {len(X_train)} | Validation: {len(X_test)}")

print("\n" + "="*60)
print("🧠 BUILDING MODEL")
print("="*60)

base_model = MobileNetV2(input_shape=(IMG_SIZE, IMG_SIZE, 3), include_top=False, weights='imagenet')
base_model.trainable = False

model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(len(LABELS), activation='softmax')
])

model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
print("✅ Model built")

print("\n" + "="*60)
print("🚂 TRAINING MODEL")
print("="*60)

history = model.fit(
    X_train, y_train,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=(X_test, y_test),
    callbacks=[EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)],
    verbose=1
)

print("\n" + "="*60)
print("📊 EVALUATING MODEL")
print("="*60)

val_loss, val_accuracy = model.evaluate(X_test, y_test)
print(f"✅ Validation Accuracy: {val_accuracy * 100:.2f}%")
print(f"✅ Validation Loss: {val_loss:.4f}")

print("\n" + "="*60)
print("💾 SAVING MODEL")
print("="*60)

os.makedirs(MODEL_OUTPUT_PATH, exist_ok=True)
model_path = os.path.join(MODEL_OUTPUT_PATH, 'keras_model.h5')
model.save(model_path)
print(f"✅ Model saved: {model_path}")

labels_path = os.path.join(MODEL_OUTPUT_PATH, 'labels.txt')
with open(labels_path, 'w') as f:
    for label in LABELS:
        f.write(f"{label}\n")
print(f"✅ Labels saved: {labels_path}")

print("\n" + "="*60)
print("✅ TRAINING COMPLETE!")
print("="*60)
print(f"📈 Final Accuracy: {val_accuracy * 100:.2f}%")
print(f"🎯 Ready to use: main_numerals.py")
print("="*60 + "\n")

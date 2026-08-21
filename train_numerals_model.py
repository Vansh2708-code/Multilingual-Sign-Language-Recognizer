import os
import numpy as np
from sklearn.model_selection import train_test_split
import cv2
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# Configuration
DATASET_PATH = 'dataset_numerals'  # Path to your numerals dataset
MODEL_OUTPUT_PATH = 'model_numerals'
IMG_SIZE = 224
BATCH_SIZE = 16  # Reduced for compatibility
EPOCHS = 50
VALIDATION_SPLIT = 0.2

# Labels for numerals
LABELS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def load_dataset(dataset_path, img_size):
    """Load images from dataset directory"""
    images = []
    labels = []
    
    for label_idx, label in enumerate(LABELS):
        label_path = os.path.join(dataset_path, label)
        
        if not os.path.exists(label_path):
            print(f"Warning: {label_path} does not exist. Skipping...")
            continue
            
        print(f"Loading images for label: {label}")
        image_files = os.listdir(label_path)
        count = 0
        
        for img_file in image_files:
            if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(label_path, img_file)
                try:
                    img = load_img(img_path, target_size=(img_size, img_size))
                    img_array = img_to_array(img)
                    img_array = preprocess_input(img_array)  # Normalize for MobileNetV2
                    images.append(img_array)
                    labels.append(label_idx)
                    count += 1
                except Exception as e:
                    print(f"Error loading {img_path}: {e}")
        
        print(f"Loaded {count} images for {label}")
    
    return np.array(images), np.array(labels)

def create_model(num_classes, img_size):
    """Create transfer learning model using MobileNetV2"""
    
    # Load pre-trained MobileNetV2 model
    base_model = MobileNetV2(
        input_shape=(img_size, img_size, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model weights
    base_model.trainable = False
    
    # Create new model
    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')
    ])
    
    return model

def train_model():
    """Main training function"""
    
    # Check if dataset exists
    if not os.path.exists(DATASET_PATH):
        print(f"Dataset path '{DATASET_PATH}' does not exist!")
        print("Please create the directory structure:")
        for label in LABELS:
            print(f"  {DATASET_PATH}/{label}/")
        return
    
    print("=" * 60)
    print("Loading dataset...")
    print("=" * 60)
    X, y = load_dataset(DATASET_PATH, IMG_SIZE)
    
    if len(X) == 0:
        print("No images found in dataset!")
        return
    
    print(f"\nTotal images loaded: {len(X)}")
    print(f"Label distribution: {np.bincount(y)}")
    
    # Split data
    print("\nSplitting data into training and validation sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=VALIDATION_SPLIT, random_state=42
    )
    
    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_test)}")
    
    # Create model
    print("\n" + "=" * 60)
    print("Creating model...")
    print("=" * 60)
    model = create_model(len(LABELS), IMG_SIZE)
    
    # Compile model
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("\nModel created successfully!")
    
    # Callbacks
    early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6)
    
    # Train model
    print("\n" + "=" * 60)
    print("Training model...")
    print("=" * 60)
    history = model.fit(
        X_train, y_train,
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=(X_test, y_test),
        callbacks=[early_stop, reduce_lr],
        verbose=1
    )
    
    # Evaluate
    print("\n" + "=" * 60)
    print("Evaluating model...")
    print("=" * 60)
    val_loss, val_accuracy = model.evaluate(X_test, y_test)
    print(f"Validation Accuracy: {val_accuracy * 100:.2f}%")
    print(f"Validation Loss: {val_loss:.4f}")
    
    # Save model
    os.makedirs(MODEL_OUTPUT_PATH, exist_ok=True)
    model_path = os.path.join(MODEL_OUTPUT_PATH, 'keras_model.h5')
    model.save(model_path)
    print(f"\n✅ Model saved to: {model_path}")
    
    # Save labels
    labels_path = os.path.join(MODEL_OUTPUT_PATH, 'labels.txt')
    with open(labels_path, 'w') as f:
        for label in LABELS:
            f.write(f"{label}\n")
    print(f"✅ Labels saved to: {labels_path}")
    
    print("\n" + "=" * 60)
    print("✅ Training Complete!")
    print("=" * 60)
    print(f"Model accuracy: {val_accuracy * 100:.2f}%")
    print(f"Ready to use with: main_numerals.py")
    print("=" * 60)


if __name__ == "__main__":
    train_model()

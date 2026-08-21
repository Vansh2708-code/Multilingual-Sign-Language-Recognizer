#!/usr/bin/env python3
"""
WORDS FEATURE - QUICK START GUIDE
Recognizes sign language words: correct, nice, you, sorry, where
"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║        MULTILINGUAL SIGN LANGUAGE RECOGNIZER - WORDS FEATURE               ║
║                          QUICK START GUIDE                                 ║
╚════════════════════════════════════════════════════════════════════════════╝

📚 WORDS TO RECOGNIZE:
   1. CORRECT - Hand gesture meaning "correct" or "right"
   2. NICE - Hand gesture expressing "nice" or appreciation
   3. YOU - Pointing gesture meaning "you"
   4. SORRY - Hand gesture expressing apology
   5. WHERE - Hand gesture asking "where"

═══════════════════════════════════════════════════════════════════════════════

🚀 STEP 1: COLLECT TRAINING DATA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run the data collection script:
   python data_collection_words.py

Instructions:
   • Show each word's sign gesture in front of the camera
   • Press 'c' to capture images (collect ~1000 per word)
   • Press 's' to skip to the next word
   • Press 'q' to quit when done

Collection Tips:
   ✓ Use good lighting
   ✓ Keep hand centered in camera view
   ✓ Vary the angle and distance slightly for better generalization
   ✓ Collect at least 500-1000 images per word

Expected Output:
   dataset_words/
   ├── correct/     (~1000 images)
   ├── nice/        (~1000 images)
   ├── you/         (~1000 images)
   ├── sorry/       (~1000 images)
   └── where/       (~1000 images)

═══════════════════════════════════════════════════════════════════════════════

🎓 STEP 2: TRAIN THE MODEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run the training script:
   python train_words_model.py

What it does:
   • Loads all images from dataset_words/
   • Uses transfer learning with MobileNetV2
   • Trains for 30 epochs (adjustable)
   • Saves model to model_words/keras_model.h5
   • Saves labels to model_words/labels.txt

Expected Training Time:
   • 15-30 minutes depending on image count and hardware
   • GPU recommended for faster training

Expected Accuracy:
   • Training accuracy: 85-95%
   • Testing accuracy: 80-90%

═══════════════════════════════════════════════════════════════════════════════

🧪 STEP 3: TEST THE MODEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Option A - Test words recognition directly:
   python main_words.py

   • Shows real-time words recognition
   • Displays confidence scores
   • Press 'q' to quit

Option B - Test in multilingual recognizer:
   python Multilingual_recognizer_with_numerals.py

   • Provides GUI with mode switching
   • Can switch between: ASL, ISL, Numerals, Words
   • Click 'Words' button to test words recognition

═══════════════════════════════════════════════════════════════════════════════

🎯 INTEGRATED MULTILINGUAL RECOGNIZER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The updated recognizer now supports 4 modes:

1. ASL MODE (American Sign Language)
   • 26 classes: A-Z letters
   • Click 'ASL' button to activate

2. ISL MODE (Indian Sign Language)
   • 26 classes: A-Z letters
   • Click 'ISL' button to activate

3. NUMERALS MODE
   • 10 classes: 0-9 digits
   • Click 'Numerals' button to activate

4. WORDS MODE
   • 5 classes: correct, nice, you, sorry, where
   • Click 'Words' button to activate

Features:
   ✓ Real-time hand detection
   ✓ Live camera feed with predictions
   ✓ Confidence scores displayed
   ✓ Color-coded display for each mode
   ✓ Smooth switching between modes

═══════════════════════════════════════════════════════════════════════════════

📊 PROJECT STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Multilingual-Sign-Language-Recognizer-master/
├── HandTrackingModule.py              (Hand detection using MediaPipe)
├── ClassificationModule.py            (Model prediction module)
│
├── 📁 Data Collection
│   ├── data_collection_asl_and_rsl.py (For ASL & RSL)
│   ├── data_collection_isl.py         (For ISL)
│   └── data_collection_words.py       (For Words) ⭐ NEW
│
├── 📁 Training Scripts
│   ├── train_numerals_model.py        (Numerals training)
│   └── train_words_model.py           (Words training) ⭐ NEW
│
├── 📁 Main Recognition Apps
│   ├── main_asl.py                    (ASL recognition)
│   ├── main_isl.py                    (ISL recognition)
│   ├── main_numerals.py               (Numerals recognition)
│   ├── main_words.py                  (Words recognition) ⭐ NEW
│   └── Multilingual_recognizer_with_numerals.py (Integrated) ⭐ UPDATED
│
├── 📁 Models
│   ├── model_asl/
│   ├── model_isl/
│   ├── model_numerals/
│   └── model_words/                   (Words model) ⭐ NEW
│
└── 📁 Datasets
    ├── dataset_asl/
    ├── dataset_isl/
    ├── dataset_numerals/
    └── dataset_words/                 (Words dataset) ⭐ NEW

═══════════════════════════════════════════════════════════════════════════════

🔧 TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Issue: "No images found" during training
   Solution: Check that dataset_words/ folder exists with subdirectories
             (correct/, nice/, you/, sorry/, where/)

Issue: Low accuracy on test set
   Solution: Collect more training data (2000+ images per word)
             Use varied angles and distances
             Ensure good lighting during collection

Issue: Model not recognizing words correctly
   Solution: Check confidence scores in real-time testing
             If <70%, collect more diverse training data
             Retrain with more epochs

Issue: Camera not detected
   Solution: Ensure webcam is connected and not in use
             Check device manager for camera availability

═══════════════════════════════════════════════════════════════════════════════

💡 TIPS FOR BEST RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Data Collection:
   ✓ Collect in consistent lighting conditions
   ✓ Use multiple people for diversity
   ✓ Include variations (left-hand, right-hand, both hands)
   ✓ Collect at least 1000 images per word

Training:
   ✓ Start with default settings, then tune hyperparameters
   ✓ Monitor validation accuracy to detect overfitting
   ✓ Use GPU for faster training if available

Recognition:
   ✓ Show full hand gesture clearly in camera
   ✓ Use consistent lighting as training
   ✓ Keep distance 0.5-1.5 meters from camera
   ✓ Hold gesture steady for 1-2 seconds

═══════════════════════════════════════════════════════════════════════════════

✅ COMPLETE WORKFLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. python data_collection_words.py
   └─> Collect ~1000 images for each of 5 words
   └─> Creates: dataset_words/{correct,nice,you,sorry,where}/

2. python train_words_model.py
   └─> Train MobileNetV2-based model
   └─> Creates: model_words/{keras_model.h5, labels.txt}

3. python main_words.py (or use Multilingual_recognizer_with_numerals.py)
   └─> Real-time recognition of: correct, nice, you, sorry, where
   └─> Display confidence scores

═══════════════════════════════════════════════════════════════════════════════

🎉 DEPLOYMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Sign Language Recognition System:
   • ASL: 26 letters
   • ISL: 26 letters
   • Numerals: 10 digits
   • Words: 5 common words (correct, nice, you, sorry, where)
   ─────────────────────────────
   TOTAL: 67 sign language gestures

Run the integrated multilingual recognizer:
   python Multilingual_recognizer_with_numerals.py

Features:
   ✓ Real-time multi-language support
   ✓ Easy mode switching via GUI buttons
   ✓ Live confidence score display
   ✓ Professional interface with Tkinter
   ✓ Optimized for accuracy and speed

═══════════════════════════════════════════════════════════════════════════════

📞 NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Options to expand further:
   1. Add more words (increase dataset_words classes)
   2. Add other sign languages (RSL - Russian Sign Language)
   3. Implement sentence recognition
   4. Add real-time translation feature
   5. Deploy as web application

═══════════════════════════════════════════════════════════════════════════════
""")

print("Ready to get started? Run: python data_collection_words.py\n")

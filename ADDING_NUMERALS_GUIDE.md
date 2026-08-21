# Guide: Adding Numerals (0-9) to Your Sign Language Recognizer

## Overview
This guide explains how to add numeral recognition (0-9) to your existing multilingual sign language recognizer project.

## Step-by-Step Instructions

### **Step 1: Create Directory Structure**

Create folders for the numerals dataset:

```
dataset_numerals/
├── 0/
├── 1/
├── 2/
├── 3/
├── 4/
├── 5/
├── 6/
├── 7/
├── 8/
└── 9/
```

PowerShell commands to create directories:
```powershell
New-Item -ItemType Directory -Path "dataset_numerals\0" -Force
New-Item -ItemType Directory -Path "dataset_numerals\1" -Force
New-Item -ItemType Directory -Path "dataset_numerals\2" -Force
New-Item -ItemType Directory -Path "dataset_numerals\3" -Force
New-Item -ItemType Directory -Path "dataset_numerals\4" -Force
New-Item -ItemType Directory -Path "dataset_numerals\5" -Force
New-Item -ItemType Directory -Path "dataset_numerals\6" -Force
New-Item -ItemType Directory -Path "dataset_numerals\7" -Force
New-Item -ItemType Directory -Path "dataset_numerals\8" -Force
New-Item -ItemType Directory -Path "dataset_numerals\9" -Force
```

### **Step 2: Collect Training Data**

Use the provided data collection script:

```bash
python "Data_collection files/data_collection_numerals.py"
```

**Instructions:**
1. Run the script
2. Hold up your hand showing the numeral sign (e.g., showing 0 with hand signs)
3. Press **'c'** to capture images (collect 100-200 images per numeral)
4. Press **'q'** when done
5. Repeat for all numerals 0-9

**Tips for better dataset:**
- Use good lighting
- Capture from different angles
- Include different hand positions
- Collect at least 100 images per numeral (more is better)

### **Step 3: Install Required Dependencies**

If not already installed, add these to your environment:

```bash
pip install scikit-learn matplotlib
```

Your `requirements.txt` should have:
```
opencv-python==4.7.0.72
tensorflow==2.12.0
mediapipe==0.9.3.0
numpy==1.23.5
scikit-learn
matplotlib
```

### **Step 4: Train the Model**

Run the training script:

```bash
python train_numerals_model.py
```

**What this does:**
- Loads all images from `dataset_numerals/` folders
- Uses transfer learning with MobileNetV2 (pre-trained on ImageNet)
- Trains a custom classifier on top of MobileNetV2
- Saves the model to `model_numerals/keras_model.h5`
- Saves labels to `model_numerals/labels.txt`
- Generates a training history plot

**Training takes approximately:**
- 15-30 minutes on CPU
- 2-5 minutes on GPU (NVIDIA)

**Expected accuracy:** 90-98% depending on dataset quality

### **Step 5: Test the Numerals Recognizer**

Run the numeral recognition script:

```bash
python main_numerals.py
```

This will show:
- Live video from your camera
- Recognized numeral
- Confidence score

### **Step 6: Use Combined Recognizer**

Run the updated multilingual recognizer with numerals support:

```bash
python Multilingual_recognizer_with_numerals.py
```

**Features:**
- Click buttons to switch between ASL, ISL, and Numerals modes
- Real-time recognition
- Shows current mode

## Project Structure After Addition

```
Multilingual-Sign-Language-Recognizer-master/
├── ClassificationModule.py
├── HandTrackingModule.py
├── train_numerals_model.py          (NEW)
├── main_numerals.py                 (NEW)
├── Multilingual_recognizer_with_numerals.py  (NEW)
├── Data_collection files/
│   ├── data_collection_numerals.py  (NEW)
│   ├── data_collection_isl.py
│   └── data_collection_asl_and_rsl.py
├── dataset_numerals/                (NEW)
│   ├── 0/
│   ├── 1/
│   ├── ... 
│   └── 9/
├── model_numerals/                  (NEW - Created after training)
│   ├── keras_model.h5
│   └── labels.txt
├── model_asl/
├── model_isl/
├── model_rsl/
└── ... (other files)
```

## Troubleshooting

### **Issue: "No Images Found in Dataset"**
- **Solution:** Make sure you've collected images in the `dataset_numerals/0/` through `dataset_numerals/9/` folders
- **Check:** Each folder should contain .jpg or .png files

### **Issue: "ModuleNotFoundError: No module named 'mediapipe'"**
- **Solution:** Install missing dependencies
```bash
pip install -r requirements.txt
```

### **Issue: Low accuracy during training**
- **Solutions:**
  - Collect more images (aim for 200+ per numeral)
  - Ensure varied angles and lighting conditions
  - Include different hand sizes and positions
  - Increase EPOCHS in `train_numerals_model.py` to 70-100

### **Issue: "IndexError: list index out of range"**
- **Solution:** Ensure the number of labels matches the number of dataset folders (should be 10 for 0-9)

## Advanced Customization

### Modify Training Parameters

Edit `train_numerals_model.py`:

```python
EPOCHS = 50              # Increase for more training iterations
BATCH_SIZE = 32          # Adjust based on RAM
VALIDATION_SPLIT = 0.2   # 20% validation, 80% training
IMG_SIZE = 224           # Must match your data
```

### Combine Numerals with Letters

To create a combined model with letters and numerals (A-Z, 0-9):

1. Create dataset folders for all 36 classes:
```
dataset_alphanumeric/
├── A/ through Z/
└── 0/ through 9/
```

2. Modify `LABELS` in `train_numerals_model.py`:
```python
LABELS = ['A', 'B', 'C', ..., 'Z', '0', '1', ..., '9']
```

3. Update the training script path accordingly

## Performance Tips

1. **GPU Acceleration:** Install `tensorflow-gpu` for faster training
2. **Reduce Training Time:** Set `EPOCHS = 20` for quick testing
3. **Improve Accuracy:**
   - Use consistent lighting during data collection
   - Collect more images (500+ per class for best results)
   - Fine-tune learning rate in training script

## Files Generated During Training

After training completes, you'll have:

```
model_numerals/
├── keras_model.h5           # The trained model
├── labels.txt               # Class labels (0-9)
└── training_history.png     # Accuracy and loss plots
```

## Next Steps

1. **Combine with existing models:** Merge numerals with your ASL/ISL models
2. **Deploy:** Create a web interface or mobile app
3. **Improve accuracy:** Collect more data and retrain
4. **Add more classes:** Follow same process for other sign classes

## References

- TensorFlow/Keras: https://www.tensorflow.org/
- MobileNetV2: https://arxiv.org/abs/1801.04381
- MediaPipe: https://mediapipe.dev/

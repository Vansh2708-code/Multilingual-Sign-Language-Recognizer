# Complete Checklist: Adding Numerals to Your Project

## ✅ Phase 1: Preparation (5 minutes)

- [ ] Read `QUICK_START_NUMERALS.md` for overview
- [ ] Ensure you have a webcam connected
- [ ] Ensure good lighting in your workspace
- [ ] Have 30-40 minutes available for data collection

## ✅ Phase 2: Setup (5 minutes)

### Create Dataset Directories
```powershell
# Open PowerShell in your project directory
0..9 | ForEach-Object { New-Item -ItemType Directory -Path "dataset_numerals\$_" -Force }
```

**Verify:** Check that folders `dataset_numerals/0` through `dataset_numerals/9` exist

### Install Dependencies (if needed)
```bash
pip install scikit-learn matplotlib
```

## ✅ Phase 3: Data Collection (30-40 minutes)

### Run Collection Script
```bash
python "Data_collection files/data_collection_numerals.py"
```

### For Each Numeral (0-9):

1. **Before starting:**
   - Edit `data_collection_numerals.py`
   - Change line 15: `folder = 'dataset_numerals/0'` (to current numeral)
   - Save file

2. **During collection:**
   - [ ] Show numeral sign to camera
   - [ ] Press 'c' to capture (target: 100-200 images)
   - [ ] Vary angles and distances
   - [ ] Include different hand sizes
   - [ ] Press 'q' to finish

3. **Repeat for all numerals 1-9**

### Target Distribution:
```
dataset_numerals/
├── 0/ - [ ] 100-200 images
├── 1/ - [ ] 100-200 images
├── 2/ - [ ] 100-200 images
├── 3/ - [ ] 100-200 images
├── 4/ - [ ] 100-200 images
├── 5/ - [ ] 100-200 images
├── 6/ - [ ] 100-200 images
├── 7/ - [ ] 100-200 images
├── 8/ - [ ] 100-200 images
└── 9/ - [ ] 100-200 images
```

**Total target:** 1000-2000 images

## ✅ Phase 4: Model Training (15-30 minutes)

### Run Training Script
```bash
python train_numerals_model.py
```

### Monitor Training:
- [ ] Check if images are loading (should show count for each numeral)
- [ ] Watch accuracy increase over epochs
- [ ] Verify validation accuracy reaches 90%+
- [ ] Check that model saves successfully

### Expected Output:
```
Loading dataset from dataset_numerals...
Loading images for label: 0
Loaded 150 images for 0
...
Total images loaded: 1500

Creating model...
Training model...

Epoch 1/50
32/32 [==============================] - 12s 375ms/step - loss: 2.1234 - accuracy: 0.3450 - val_loss: 1.8765 - val_accuracy: 0.4567

...

Epoch 50/50
32/32 [==============================] - 8s 250ms/step - loss: 0.1234 - accuracy: 0.9876 - val_loss: 0.1567 - val_accuracy: 0.9654

Validation Accuracy: 96.54%
Model saved to: model_numerals/keras_model.h5
Labels saved to: model_numerals/labels.txt
```

### Files Created:
- [ ] `model_numerals/keras_model.h5` (20-30 MB)
- [ ] `model_numerals/labels.txt` (10 lines)
- [ ] `model_numerals/training_history.png` (graph)

## ✅ Phase 5: Testing (5 minutes)

### Test Numerals Only
```bash
python main_numerals.py
```

- [ ] Show numeral to camera
- [ ] Verify correct recognition
- [ ] Check confidence score
- [ ] Test all numerals 0-9
- [ ] Press 'q' to close

### Expected:
```
Numeral Recognition System Started
Press 'q' to quit

# Window shows:
- Live video
- Recognized numeral (e.g., "5")
- Confidence score (e.g., "Confidence: 0.98")
```

## ✅ Phase 6: Integration (2 minutes)

### Run Full Multilingual App
```bash
python Multilingual_recognizer_with_numerals.py
```

- [ ] Click "Numerals" button
- [ ] Test recognition in numerals mode
- [ ] Click "ASL" button (should switch to ASL)
- [ ] Click "ISL" button (should switch to ISL)
- [ ] Click "Numerals" again
- [ ] Close app (press Alt+F4)

## ✅ Phase 7: Optimization (Optional)

### If Accuracy is Low (< 85%):

1. [ ] Collect more data (target 250+ per numeral)
2. [ ] Ensure good lighting during collection
3. [ ] Increase EPOCHS in `train_numerals_model.py` to 100
4. [ ] Retrain model

### If Training is Slow:

1. [ ] Install GPU support: `pip install tensorflow-gpu`
2. [ ] Or reduce BATCH_SIZE from 32 to 16

## ✅ Phase 8: Documentation (Optional)

- [ ] Read `ADDING_NUMERALS_GUIDE.md` for advanced options
- [ ] Read `GENERIC_TRAINING_TEMPLATE.md` for adding other classes
- [ ] Save these guides for future reference

## Common Issues Checklist

### Issue: "No Images Found"
- [ ] Verify dataset_numerals/ folder exists
- [ ] Check folders 0-9 have images inside
- [ ] File extensions should be .jpg or .png

### Issue: "ModuleNotFoundError"
- [ ] Run: `pip install -r requirements.txt`
- [ ] Run: `pip install scikit-learn matplotlib`
- [ ] Verify Python version is 3.7+

### Issue: Low Accuracy (< 80%)
- [ ] Collect more images (minimum 150 per class)
- [ ] Check lighting is consistent
- [ ] Train longer: change EPOCHS to 100
- [ ] Ensure no corruption in images

### Issue: Out of Memory
- [ ] Reduce BATCH_SIZE from 32 to 16
- [ ] Close other applications
- [ ] Train on smaller dataset first

### Issue: Camera Not Working
- [ ] Change camera ID in scripts (0 → 1)
- [ ] Test with: `python -c "import cv2; cv2.VideoCapture(0).release()"`
- [ ] Ensure no other app uses webcam

### Issue: Model Not Found
- [ ] Verify training completed successfully
- [ ] Check model_numerals/ folder exists
- [ ] Run training script again if needed

## Success Criteria

✅ **Project Complete When:**
- [ ] All 10 numerals have 100+ training images
- [ ] Training completed with 90%+ accuracy
- [ ] `main_numerals.py` recognizes numerals correctly
- [ ] `Multilingual_recognizer_with_numerals.py` switches modes
- [ ] All buttons work in full app

## Timeline

| Phase | Time | Status |
|-------|------|--------|
| Preparation | 5 min | ⏳ |
| Setup | 5 min | ⏳ |
| Data Collection | 30-40 min | ⏳ |
| Training | 15-30 min | ⏳ |
| Testing | 5 min | ⏳ |
| Integration | 2 min | ⏳ |
| **Total** | **60-90 min** | ⏳ |

## Next Steps After Completion

1. **Improve accuracy:**
   - Collect more data (500+ per class)
   - Fine-tune model parameters

2. **Add more classes:**
   - Follow same process for letters, colors, objects, etc.
   - Use `GENERIC_TRAINING_TEMPLATE.md`

3. **Combine models:**
   - Create multi-modal recognizer
   - Combine numerals + letters + other gestures

4. **Deploy:**
   - Create web interface
   - Build mobile app
   - Deploy to cloud

## Document References

| Document | Purpose | When to Use |
|----------|---------|------------|
| `QUICK_START_NUMERALS.md` | Fast reference | First time |
| `ADDING_NUMERALS_GUIDE.md` | Detailed guide | Need details |
| `GENERIC_TRAINING_TEMPLATE.md` | Add other classes | Adding new gestures |
| `IMPLEMENTATION_SUMMARY.md` | Full overview | Reference |
| This file | Step-by-step | During implementation |

---

## Support

If you get stuck:
1. Check the troubleshooting section above
2. Read the detailed guide: `ADDING_NUMERALS_GUIDE.md`
3. Check generic template: `GENERIC_TRAINING_TEMPLATE.md`
4. Verify all prerequisites installed: `pip install -r requirements.txt`

**Good luck! 🚀**

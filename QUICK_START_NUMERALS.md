# Quick Start: Training Numerals

## Quick Commands

### 1. Create Dataset Directories
```powershell
0..9 | ForEach-Object { New-Item -ItemType Directory -Path "dataset_numerals\$_" -Force }
```

### 2. Collect Data
```bash
python "Data_collection files/data_collection_numerals.py"
```
- Show each numeral sign (0-9)
- Press 'c' to capture (100-200 images per numeral)
- Press 'q' when done

### 3. Train Model
```bash
python train_numerals_model.py
```
- Automatic: Loads data → Trains → Saves model
- Output: `model_numerals/keras_model.h5` + `model_numerals/labels.txt`

### 4. Test Recognition
```bash
python main_numerals.py
```

### 5. Use in Full App
```bash
python Multilingual_recognizer_with_numerals.py
```

## What Each Script Does

| Script | Purpose |
|--------|---------|
| `data_collection_numerals.py` | Collect training images for numerals |
| `train_numerals_model.py` | Train the neural network model |
| `main_numerals.py` | Test numerals only |
| `Multilingual_recognizer_with_numerals.py` | Full app with ASL, ISL, and Numerals |

## Folder Structure
```
dataset_numerals/     ← Your training data
    0/ (100+ images)
    1/ (100+ images)
    ... 
    9/ (100+ images)
    
model_numerals/       ← Generated after training
    keras_model.h5
    labels.txt
```

## Time Required

| Task | Time |
|------|------|
| Collect data (all numerals) | 20-30 minutes |
| Train model (CPU) | 15-30 minutes |
| Train model (GPU) | 2-5 minutes |
| Test recognition | Instant |

## Key Parameters to Adjust

File: `train_numerals_model.py`

```python
EPOCHS = 50              # More = better accuracy but slower (try 100)
BATCH_SIZE = 32          # Reduce if out of memory
IMG_SIZE = 224           # Must match data (don't change)
VALIDATION_SPLIT = 0.2   # 20% for testing, 80% for training
```

## Expected Results

- **Accuracy:** 90-98%
- **Model Size:** ~20-30 MB
- **Training Time:** 15-30 min (CPU) or 2-5 min (GPU)

## Troubleshooting

**Q: Model not found error**
A: Run `train_numerals_model.py` first to create the model

**Q: Low accuracy**
A: Collect more images (200+ per numeral), retrain with more epochs

**Q: Out of memory error**
A: Reduce `BATCH_SIZE` from 32 to 16 or 8

**Q: Only 1 numeral works**
A: Ensure all 10 folders (0-9) have training images

## Advanced: Combine Models

To use numerals + letters (A-Z + 0-9):

1. Create `dataset_combined/` with folders: A-Z, 0-9
2. Modify LABELS in training script
3. Run training script
4. Update recognizer to use new model

---

**For detailed instructions, see: `ADDING_NUMERALS_GUIDE.md`**

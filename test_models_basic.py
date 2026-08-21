#!/usr/bin/env python3
"""
Basic model testing without camera access
Tests if models can be loaded and basic predictions work
"""

import numpy as np
from ClassificationModule import Classifier
import sys

def test_model_loading():
    """Test if all models can be loaded successfully"""
    print("="*60)
    print("MULTILINGUAL SIGN LANGUAGE RECOGNIZER - MODEL TEST")
    print("="*60)
    
    models = [
        ("ASL", "model_asl/keras_model.h5", "model_asl/labels.txt"),
        ("ISL", "model_isl/keras_model.h5", "model_isl/labels.txt"),
        ("Numerals", "model_numerals/keras_model.h5", "model_numerals/labels.txt"),
        ("Words", "model_words/keras_model.h5", "model_words/labels.txt")
    ]
    
    loaded_models = {}
    
    for name, model_path, labels_path in models:
        try:
            print(f"\nLoading {name} model...")
            classifier = Classifier(model_path, labels_path)
            loaded_models[name] = classifier
            
            # Test with dummy data
            dummy_img = np.ones((224, 224, 3), dtype=np.uint8) * 128
            prediction, index = classifier.getPrediction(dummy_img, draw=False)
            
            print(f"[OK] {name} model loaded successfully")
            print(f"  - Model shape: {classifier.model.input_shape}")
            print(f"  - Number of classes: {len(classifier.list_labels)}")
            print(f"  - Sample prediction shape: {len(prediction)}")
            
        except Exception as e:
            print(f"[FAIL] Failed to load {name} model: {e}")
            return False
    
    print(f"\n{'='*60}")
    print("ALL MODELS LOADED SUCCESSFULLY!")
    print(f"{'='*60}")
    
    # Display available labels for each model
    print("\nAvailable labels:")
    for name, classifier in loaded_models.items():
        print(f"  {name}: {classifier.list_labels}")
    
    return True

def main():
    success = test_model_loading()
    
    if success:
        print("\n" + "="*60)
        print("STATUS: READY TO RUN")
        print("="*60)
        print("\nTo run the full application:")
        print("1. Ensure camera access is available")
        print("2. Run: python Multilingual_recognizer_with_numerals.py")
        print("\nFeatures available:")
        print("- ASL (American Sign Language) - Letters A-Z")
        print("- ISL (Indian Sign Language) - Letters A-Z") 
        print("- Numerals (0-9)")
        print("- Words (correct, nice, you, sorry, where)")
        print("\n" + "="*60)
    else:
        print("\n" + "="*60)
        print("STATUS: MODEL LOADING FAILED")
        print("="*60)
        sys.exit(1)

if __name__ == "__main__":
    main()
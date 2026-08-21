# 🌐 Multilingual Sign Language Recognizer

An AI-powered, real-time sign language recognition system designed to recognize **American Sign Language (ASL), Indian Sign Language (ISL), numerals (0–9), and selected Indian words** using static hand gestures.

The system uses **Python, OpenCV, MediaPipe, and deep learning models** to detect hand gestures through a webcam and convert recognized gestures into meaningful outputs. It is designed to support affordable, accessible, and locally deployable sign language recognition.

---

## 🚀 Features

* 🤟 **ASL Recognition**
* 🇮🇳 **ISL Recognition**
* 🔢 **Numeral Recognition (0–9)**
* 🗣️ **Selected Indian Word Recognition**
* 📷 Real-time webcam-based recognition
* ✋ MediaPipe-based hand detection
* 🧠 Deep learning-based gesture classification
* 🖥️ Tkinter-based graphical interface
* 🔄 Easy switching between ASL, ISL, and Numeral modes
* 📊 Confidence-score display
* 📴 Local processing without mandatory cloud connectivity
* 📚 Complete data collection and model-training pipeline

The multilingual application combines ASL, ISL, and numeral recognition into a single interface with dedicated mode-selection buttons.

---

## 🧠 Technologies Used

| Technology                  | Purpose                              |
| --------------------------- | ------------------------------------ |
| **Python**                  | Core development                     |
| **OpenCV**                  | Image and webcam processing          |
| **MediaPipe**               | Hand detection and landmark tracking |
| **TensorFlow / Keras**      | Deep learning model training         |
| **CNN / Transfer Learning** | Gesture classification               |
| **NumPy**                   | Numerical processing                 |
| **Tkinter**                 | Graphical user interface             |
| **Text-to-Speech**          | Speech output                        |
| **Raspberry Pi**            | Edge-device deployment               |

---

## 🏗️ System Workflow

```text
          📷 Webcam
              │
              ▼
      ┌─────────────────┐
      │     OpenCV      │
      │ Video Capture   │
      └────────┬────────┘
               │
               ▼
      ┌─────────────────┐
      │    MediaPipe    │
      │  Hand Detection │
      └────────┬────────┘
               │
               ▼
      ┌─────────────────┐
      │ Preprocessing & │
      │ Feature/Input   │
      │    Handling     │
      └────────┬────────┘
               │
               ▼
      ┌─────────────────┐
      │ Deep Learning   │
      │ Classification  │
      └────────┬────────┘
               │
       ┌───────┼────────┬───────────┐
       ▼       ▼        ▼           ▼
      ASL     ISL    Numerals    ISL Static 
                       0–9         Words
               │
               ▼
      ┌─────────────────┐
      │ Recognized Sign │
      └────────┬────────┘
               │
          ┌────┴────┐
          ▼         ▼
        📝 Text    🔊 Speech
```

---


```

The numeral implementation includes dedicated data collection, training, testing, and multilingual recognition scripts.

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/Multilingual-Sign-Language-Recognizer.git
cd Multilingual-Sign-Language-Recognizer
```

### 2. Install Dependencies

```bash
pip install opencv-python mediapipe tensorflow numpy
```

If your project contains a requirements file:

```bash
pip install -r requirements.txt
```

### 3. Run Numeral Recognition

```bash
python main_numerals.py
```

### 4. Run the Multilingual Recognizer

```bash
python Multilingual_recognizer_with_numerals.py
```

---

## 🔢 Training the Numeral Model

The project includes a complete pipeline for training a model to recognize numerals from **0 to 9**.

### Collect Training Data

```bash
python "data_collection_files/data_collection_numerals.py"
```

The data collection system uses the webcam and saves captured images into the corresponding numeral directories. The `c` key captures an image and `q` exits the application.

### Train the Model

```bash
python train_numerals_model.py
```

The training pipeline uses **MobileNetV2 transfer learning, data augmentation, early stopping, and learning-rate reduction**.

### Test the Model

```bash
python main_numerals.py
```

---

## 🎮 Controls

### Numeral Recognition

| Key | Action                 |
| --- | ---------------------- |
| `q` | Exit application       |
| `c` | Capture training image |

### Multilingual Interface

| Button       | Mode                   |
| ------------ | ---------------------- |
| **ASL**      | American Sign Language |
| **ISL**      | Indian Sign Language   |
| **Numerals** | Numbers 0–9            |

The multilingual interface provides real-time recognition with GUI-based mode switching.

---

## 📊 Training Pipeline

```text
Collect Images
      ↓
Organize Dataset
      ↓
Preprocess Images
      ↓
Data Augmentation
      ↓
Transfer Learning
      ↓
Model Training
      ↓
Validation
      ↓
Save Model
      ↓
Real-Time Recognition
```

The documented numeral workflow estimates approximately **30–40 minutes for data collection, 15–30 minutes for training, and 5 minutes for testing**, depending on the system and dataset.

---

## 🎯 Current Recognition Scope

The current system focuses primarily on **static hand gestures**.

### Supported Categories

* 🇺🇸 American Sign Language (ASL)
* 🇮🇳 Indian Sign Language (ISL)
* 🔢 Numerals 0–9
* 🗣️ Selected Indian words
* 🤟 Additional trained gesture classes

---

## 📈 Model Development

The project provides a reusable workflow for adding additional gesture classes. The included generic training template can be adapted for letters, common gestures, objects, emotions, and other custom categories.

---

## 🔮 Future Enhancements

* [ ] Dynamic sign language recognition
* [ ] Continuous sentence recognition
* [ ] Larger ISL vocabulary
* [ ] More Indian regional sign languages
* [ ] Improved model accuracy
* [ ] Raspberry Pi optimization
* [ ] Mobile application
* [ ] Web-based interface
* [ ] Automatic sentence formation
* [ ] Advanced text-to-speech
* [ ] Real-time conversational translation

---

## 📚 Documentation

| Document                       | Purpose                            |
| ------------------------------ | ---------------------------------- |
| `START_HERE.md`                | Introduction and first-time setup  |
| `QUICK_START_NUMERALS.md`      | Quick commands and setup           |
| `ADDING_NUMERALS_GUIDE.md`     | Detailed numeral implementation    |
| `GENERIC_TRAINING_TEMPLATE.md` | Adding new gesture classes         |
| `CHECKLIST.md`                 | Development checklist              |
| `VISUAL_WORKFLOW.md`           | Architecture and workflow diagrams |
| `IMPLEMENTATION_SUMMARY.md`    | Complete implementation overview   |

The repository includes multiple documentation paths covering quick setup, detailed implementation, visual workflows, troubleshooting, and future class expansion.

---

## 🤝 Contributing

Contributions are welcome!

You can contribute by:

1. Forking this repository.
2. Creating a new branch.
3. Adding improvements or new gesture classes.
4. Testing your changes.
5. Creating a Pull Request.

---

## 📜 License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for details.

> **Note:** The project's source code license does not automatically determine the license of external datasets, pretrained models, or third-party dependencies. Check the respective licenses before redistributing them.

---

## 👨‍💻 Project

**Multilingual Sign Language Recognizer**

Built with ❤️ using **Python, Computer Vision, Deep Learning, and Edge AI**.

⭐ If you find this project useful, consider giving the repository a **star**!

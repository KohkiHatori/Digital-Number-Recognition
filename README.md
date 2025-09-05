# Alcohol Detection System for Transportation Safety 🚛🔍

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com)
[![MMDetection](https://img.shields.io/badge/MMDetection-2.7.0-orange.svg)](https://github.com/open-mmlab/mmdetection)

> An ML model that automates alcohol level detection from digital display images to ensure transportation safety compliance in Japan.

## 🎯 Project Overview

This project was developed during my 2-week ML engineering internship at **Second Xight Analytica** in Tokyo (Summer 2022). The system addresses the mandatory alcohol checking requirements for transportation drivers that became effective in Japan from April 2022.

**What it does**: Automatically reads digital numbers from alcohol detector displays using computer vision and determines whether the detected alcohol level exceeds legal limits.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Scraping  │ →  │  Data Labeling  │ →  │  Model Training │
│   (~1000 imgs)  │    │   (Manual +     │    │  (Cascade R-CNN)│
│                 │    │   Auto-labeling)│    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
          │                       │                       │
          └───────────────────────┼───────────────────────┘
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Deployment Pipeline                         │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   FastAPI       │   Web Frontend  │     Annotation Tool         │
│   Backend       │   (HTML/CSS/JS) │   (Error Correction)        │
│                 │                 │                             │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

## 🔧 Technology Stack

- **Computer Vision**: MMDetection (OpenMMLab), Cascade R-CNN with ResNeXt-101 backbone
- **Backend API**: FastAPI, Python 3.8+
- **Frontend**: Vanilla HTML, CSS, JavaScript with jQuery
- **Data Collection**: Web scraping with BeautifulSoup, requests
- **Image Processing**: OpenCV, PIL
- **Model Framework**: PyTorch

## 📊 Project Components

### 1. Data Collection (`1_scraping/`)
- **Web scraper** that collects ~1000 images of digital displays
- Searches for alcohol detectors, digital clocks, calculators, and scales
- Multi-language support (Japanese/English) with automatic detection
- SSL-secured image downloading with error handling

### 2. ML Model (`3_model/`)
- **Cascade Mask R-CNN** with ResNeXt-101-64x4d-FPN backbone
- Custom configuration for digit detection (0-9) and decimal point recognition
- Trained on 1000 manually and automatically labeled images
- Confidence threshold tuning for optimal accuracy

### 3. API & Web Interface (`2_API/`)
- **FastAPI backend** with async image processing endpoints
- **Drag-and-drop web interface** for easy image uploads
- **Real-time prediction** display with confidence scores
- **Annotation correction tool** for improving model accuracy
- Image storage and result logging capabilities

## 🎯 Key Technical Challenges & Solutions

### Challenge 1: Decimal Point Recognition
**Problem**: Small image sizes made decimal point detection extremely difficult  
**Solution**: 
- Improved manual labeling accuracy for the initial 100 training images
- Implemented iterative refinement process for auto-labeling
- Fine-tuned confidence thresholds specifically for punctuation marks

### Challenge 2: Digit Misrecognition (2s and 5s)
**Problem**: Random horizontal flipping during training caused 2s and 5s to be frequently misidentified  
**Solution**: 
- Set horizontal flip probability to 0 in data augmentation pipeline
- Retrained model with corrected augmentation parameters
- Achieved significant improvement in digit classification accuracy

### Challenge 3: Auto-labeling Accuracy
**Problem**: Quality of initial 100 manual labels directly affected remaining 900 auto-labels  
**Solution**:
- Implemented multiple validation rounds for manual labels
- Created feedback loop between manual and automatic labeling
- Iterative refinement process with quality checkpoints

## 📈 Results & Impact

- ✅ Successfully developed automated alcohol level detection system
- ✅ Built complete ML pipeline from data collection to inference
- ✅ Achieved high accuracy on digit recognition tasks
- ✅ Created functional web interface for demonstration
- ✅ Built annotation correction tool for model improvement

## 🎥 Demo Features

### Web Interface
- **Drag-and-drop image upload** with real-time preview
- **Prediction display** showing detected digits and confidence scores
- **Interactive annotation tool** for model improvement and validation
- **Responsive design** built with vanilla HTML, CSS, and JavaScript

### Backend API
- **FastAPI endpoints** for image processing and prediction
- **Asynchronous processing** for handling multiple image uploads
- **Model inference pipeline** with configurable confidence thresholds
- **Data logging and storage** for continuous model improvement

*Note: Trained model files are not included in the repository due to size constraints (stored in `3_model/` - see `.gitignore`).*

## 📁 Project Structure

```
sxi/
├── 1_scraping/          # Web scraping for data collection
│   └── scrape.py       # Google Images scraper
├── 2_API/              # FastAPI backend & frontend
│   ├── alcohol_api.py  # Main API server
│   ├── predict.py      # Prediction logic
│   ├── templates/      # HTML templates
│   ├── static/         # CSS/JS assets
│   ├── images/         # Sample images
│   └── llib/           # MMDetection utilities
├── 3_model/            # Trained model files (excluded from repo)
│   ├── latest.pth      # Latest checkpoint (not in repo)
│   └── epoch_15.pth    # Specific epoch checkpoint (not in repo)
└── sxi_env/            # Virtual environment
```

## 🔍 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload` | GET | Main upload interface |
| `/process` | POST | Process uploaded images |
| `/fix` | GET | Annotation correction tool |
| `/save_img` | POST | Save images for labeling |
| `/test` | GET | API health check |

## 🎓 Learning Outcomes

This internship provided invaluable hands-on experience in:

- **End-to-end ML pipeline development** from data collection to model training
- **Computer vision model fine-tuning** with real-world constraints
- **ML system architecture** and inference pipeline design
- **Web development** for ML applications and demonstrations
- **Problem-solving** in challenging computer vision scenarios

The project highlighted the close relationship between theory and practice in the IT industry, demonstrating how academic knowledge translates directly into real-world solutions.

## 🔮 Future Enhancements

- [ ] **Production deployment** with cloud infrastructure
- [ ] **Mobile app development** for on-the-go detection
- [ ] **Real-time video processing** for continuous monitoring
- [ ] **Model optimization** for edge device deployment
- [ ] **Integration with IoT devices** for automated checking

## 🏢 Company Information

**Second Xight Analytica**  
Location: Otemachi, Tokyo, Japan  
Industry: ML/Data Science Startup  
Internship Duration: 2 weeks (Summer 2022)  
Role: ML Engineer Intern

## 📞 Contact

**Kohki Hatori**  
- Email: [khatori@bu.edu]
<!-- - LinkedIn: [Your LinkedIn Profile]
- Portfolio: [Your Portfolio Website] -->

---

*This project demonstrates practical application of computer vision technologies in regulatory compliance, showcasing the potential of machine learning to solve real-world transportation safety challenges.*

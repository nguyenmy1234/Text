# 02_Text - Amazon Reviews Text Analysis

## Project Overview
This project performs comprehensive text analysis and classification on Amazon product reviews using Natural Language Processing (NLP) techniques.

## Directory Structure
```
02_Text/
├── requirements.txt              # Project dependencies
├── scripts/
│   ├── prepare_amazon_dataset.py # Data preparation script
│   └── nb_parts/
│       ├── part3_modeling.py     # Text classification models
│       ├── part4_summary.py      # Results and visualization
│       └── notes.py              # Project notes
├── notebooks/
│   └── 02_Text_Amazon_Reviews.ipynb  # Jupyter notebook for analysis
└── README.md                    # This file
```

## Requirements
- Python 3.8+
- numpy
- pandas
- scikit-learn
- matplotlib
- seaborn
- nltk
- tensorflow/keras

## Installation
```bash
pip install -r requirements.txt
```

## Usage

### 1. Prepare Data
```bash
python scripts/prepare_amazon_dataset.py
```

### 2. Run Analysis
Open and run the Jupyter notebook:
```bash
jupyter notebook notebooks/02_Text_Amazon_Reviews.ipynb
```

### 3. Train Models
The modeling pipeline includes:
- TF-IDF vectorization
- Naive Bayes classification
- Model evaluation and metrics

## Key Features
- **Text Preprocessing**: Cleaning and normalization of review text
- **Feature Extraction**: TF-IDF vectorization
- **Classification**: Naive Bayes model for sentiment/rating prediction
- **Evaluation**: Accuracy metrics and performance analysis
- **Visualization**: Rating and text length distributions

## Results
See `scripts/nb_parts/part4_summary.py` for detailed results and visualizations.

## Notes
Refer to `scripts/nb_parts/notes.py` for project observations and future improvements.

## Author
nguyenmy1234

## License
MIT

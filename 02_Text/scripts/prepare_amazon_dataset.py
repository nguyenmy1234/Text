# Amazon Dataset Preparation Script
# This script prepares the Amazon reviews dataset for text analysis

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def load_data(filepath):
    """Load Amazon reviews data"""
    return pd.read_csv(filepath)

def preprocess_text(text):
    """Clean and preprocess text data"""
    # Remove special characters, lowercase
    return text.lower().strip()

def prepare_dataset(df):
    """Prepare dataset for modeling"""
    df['processed_text'] = df['review'].apply(preprocess_text)
    return df

if __name__ == '__main__':
    print('Amazon dataset preparation script')
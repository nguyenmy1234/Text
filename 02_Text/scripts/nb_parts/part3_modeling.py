# Part 3: Text Modeling
# Machine learning models for text classification

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd

def create_text_classifier():
    """Create TF-IDF + Naive Bayes pipeline"""
    return Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000)),
        ('clf', MultinomialNB())
    ])

def train_model(X_train, y_train):
    """Train the text classification model"""
    clf = create_text_classifier()
    clf.fit(X_train, y_train)
    return clf

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    score = model.score(X_test, y_test)
    print(f'Model Accuracy: {score:.4f}')
    return score

if __name__ == '__main__':
    print('Text Modeling Module')
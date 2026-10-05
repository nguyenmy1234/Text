# Part 4: Summary and Results
# Summarize findings and results from text analysis

import pandas as pd
import matplotlib.pyplot as plt

def generate_summary_statistics(df):
    """Generate summary statistics from processed data"""
    summary = {
        'total_reviews': len(df),
        'avg_rating': df['rating'].mean(),
        'avg_text_length': df['text'].str.len().mean()
    }
    return summary

def create_visualizations(df):
    """Create summary visualizations"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Rating distribution
    df['rating'].value_counts().sort_index().plot(ax=axes[0], kind='bar')
    axes[0].set_title('Rating Distribution')
    
    # Text length distribution
    df['text'].str.len().hist(ax=axes[1], bins=50)
    axes[1].set_title('Text Length Distribution')
    
    plt.tight_layout()
    return fig

if __name__ == '__main__':
    print('Summary and Results Module')
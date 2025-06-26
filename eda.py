import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from data_pipeline import DataLoader, DataCleaner, DataPreprocessor
from wordcloud import WordCloud

# Create a directory to save plots
if not os.path.exists('plots'):
    os.makedirs('plots')

def load_and_preprocess_data(filepath):
    """
    Loads and preprocesses the data using the data pipeline.
    
    :param filepath: Path to the JSON dataset file.
    :return: A preprocessed pandas DataFrame.
    """
    loader = DataLoader(filepath)
    df = loader.to_dataframe()
    
    cleaner = DataCleaner(df)
    cleaned_df = cleaner.clean_data()
    
    preprocessor = DataPreprocessor(cleaned_df)
    processed_df = preprocessor.transform_data()
    
    return processed_df

def generate_summary_statistics(df):
    """
    Generates and prints summary statistics of the dataset.
    
    :param df: The pandas DataFrame to analyze.
    """
    print("--- High-Level Summary Statistics ---")
    # For object columns, provide frequency-based stats
    print(df.describe(include=['object', 'category']))
    print("\n")
    
    # Article-level summary
    print("--- Article-Level Summary ---")
    article_summary = df.groupby('article_url').agg(
        total_turns=('transcript_id', 'count'),
        num_agents=('agent', 'nunique')
    ).sort_values(by='total_turns', ascending=False)
    print(article_summary.head())
    print("\n")

    # Agent-level summary
    print("--- Agent-Level Summary ---")
    agent_summary = df.groupby('agent').agg(
        total_messages=('message', 'count'),
        avg_message_length=('processed_message', lambda x: x.str.len().mean())
    )
    # Sentiment distribution per agent
    sentiment_dist = df.groupby(['agent', 'sentiment']).size().unstack(fill_value=0)
    agent_summary = agent_summary.join(sentiment_dist)
    print(agent_summary)
    print("\n")

def plot_message_distribution(df):
    """
    Plots the distribution of messages per agent.
    
    :param df: The pandas DataFrame to analyze.
    """
    plt.figure(figsize=(8, 6))
    sns.countplot(x='agent', data=df, palette='viridis')
    plt.title('Number of Messages per Agent')
    plt.xlabel('Agent')
    plt.ylabel('Number of Messages')
    plt.savefig('plots/messages_per_agent.png')
    plt.close()
    print("Plot 'messages_per_agent.png' saved to /plots directory.")

def plot_sentiment_distribution(df):
    """
    Plots the distribution of sentiments per agent.
    
    :param df: The pandas DataFrame to analyze.
    """
    plt.figure(figsize=(12, 8))
    sns.countplot(y='sentiment', hue='agent', data=df, palette='magma')
    plt.title('Sentiment Distribution per Agent')
    plt.xlabel('Count')
    plt.ylabel('Sentiment')
    plt.tight_layout()
    plt.savefig('plots/sentiment_per_agent.png')
    plt.close()
    print("Plot 'sentiment_per_agent.png' saved to /plots directory.")

def plot_turn_rating_distribution(df):
    """
    Plots the distribution of turn ratings.
    
    :param df: The pandas DataFrame to analyze.
    """
    plt.figure(figsize=(10, 6))
    sns.countplot(x='turn_rating', data=df, palette='rocket')
    plt.title('Distribution of Turn Ratings')
    plt.xlabel('Turn Rating')
    plt.ylabel('Count')
    plt.savefig('plots/turn_rating_distribution.png')
    plt.close()
    print("Plot 'turn_rating_distribution.png' saved to /plots directory.")

def plot_conversation_length_distribution(df):
    """
    Plots the distribution of conversation lengths (turns per transcript).
    
    :param df: The pandas DataFrame to analyze.
    """
    conv_lengths = df.groupby('transcript_id').size()
    plt.figure(figsize=(10, 6))
    sns.histplot(conv_lengths, bins=20, kde=True)
    plt.title('Distribution of Conversation Lengths (Turns per Transcript)')
    plt.xlabel('Number of Turns')
    plt.ylabel('Frequency')
    plt.savefig('plots/conversation_length_distribution.png')
    plt.close()
    print("Plot 'conversation_length_distribution.png' saved to /plots directory.")

def generate_word_cloud(df):
    """
    Generates and saves a word cloud from the processed messages.
    
    :param df: The pandas DataFrame to analyze.
    """
    text = " ".join(review for review in df.processed_message)
    wordcloud = WordCloud(
        max_words=100,
        background_color="white",
        width=800,
        height=400,
    ).generate(text)
    
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title('Most Frequent Words in Conversations')
    plt.savefig('plots/word_cloud.png')
    plt.close()
    print("Plot 'word_cloud.png' saved to /plots directory.")

def generate_simple_word_cloud(df):
    """
    Generates and saves a simpler, more readable word cloud.
    
    :param df: The pandas DataFrame to analyze.
    """
    text = " ".join(review for review in df.processed_message)
    wordcloud = WordCloud(
        max_words=50,  # Fewer words
        background_color="white",
        width=800,
        height=400,
        colormap='viridis',  # A different color scheme
        collocations=False  # Avoids grouping words
    ).generate(text)
    
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title('Most Frequent Words in Conversations (Simple Word Cloud)')
    plt.savefig('plots/word_cloud_simple.png')
    plt.close()
    print("Plot 'word_cloud_simple.png' saved to /plots directory.")

def plot_top_words_barchart(df, top_n=20):
    """
    Plots the most frequent words in a bar chart for better readability.
    
    :param df: The pandas DataFrame containing the 'processed_message' column.
    :param top_n: The number of top words to display.
    """
    all_words = " ".join(msg for msg in df.processed_message).split()
    top_words_df = pd.Series(all_words).value_counts().nlargest(top_n).reset_index()
    top_words_df.columns = ['word', 'count']
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x='count', y='word', data=top_words_df, palette='plasma')
    plt.title(f'Top {top_n} Most Frequent Words (Bar Chart)')
    plt.xlabel('Frequency')
    plt.ylabel('Word')
    plt.tight_layout()
    plt.savefig('plots/top_words_barchart.png')
    plt.close()
    print("Plot 'top_words_barchart.png' saved to /plots directory.")


if __name__ == '__main__':
    DATA_FILE = 'BiztelAI_DS_Dataset_V1.json'
    
    df = load_and_preprocess_data(DATA_FILE)
    
    generate_summary_statistics(df)
    
    plot_message_distribution(df)
    plot_sentiment_distribution(df)
    plot_turn_rating_distribution(df)
    plot_conversation_length_distribution(df)
    generate_word_cloud(df)
    generate_simple_word_cloud(df)
    plot_top_words_barchart(df)
    
    print("\nEDA script finished. Check the /plots directory for visualizations.") 
import json
import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.preprocessing import LabelEncoder

# Force-load resources in the main thread
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
_ = stopwords.words('english')
_ = WordNetLemmatizer()

class DataLoader:
    """
    Handles loading the dataset from a JSON file.
    """
    def __init__(self, filepath):
        """
        Initializes the DataLoader with the path to the dataset.
        
        :param filepath: Path to the JSON dataset file.
        """
        self.filepath = filepath
        self.raw_data = None

    def load_data(self):
        """
        Loads the JSON data from the specified file.
        
        :return: The loaded raw JSON data.
        """
        with open(self.filepath, 'r') as f:
            self.raw_data = json.load(f)
        return self.raw_data

    def to_dataframe(self):
        # Converts the nested JSON data into a Pandas DataFrame. :return: A pandas DataFrame with flattened data.
        if self.raw_data is None:
            self.load_data()
            
        records = []
        for transcript_id, data in self.raw_data.items():
            article_url = data.get('article_url')
            for turn in data.get('content', []):
                record = {
                    'transcript_id': transcript_id,
                    'article_url': article_url,
                    'message': turn.get('message'),
                    'agent': turn.get('agent'),
                    'sentiment': turn.get('sentiment'),
                    'knowledge_source': turn.get('knowledge_source'),
                    'turn_rating': turn.get('turn_rating')
                }
                records.append(record)
                
        return pd.DataFrame(records)

class DataCleaner:
    """
    Handles cleaning the DataFrame.
    """
    def __init__(self, df):
        """
        Initializes the DataCleaner with a DataFrame.
        
        :param df: The pandas DataFrame to clean.
        """
        self.df = df.copy()

    def remove_duplicates(self):
        # We identify duplicates based on a subset of columns that uniquely identify a turn,
        # excluding any unhashable columns like 'knowledge_source'.
        self.df.drop_duplicates(subset=['transcript_id', 'agent', 'message'], inplace=True)
        return self

    def handle_missing_values(self):
    
        # Handles missing values in the DataFrame.
        # Rows with missing 'message' or 'agent' are dropped. We cant replace them or fill them. if they were numerical then it would be different.
    
        self.df.dropna(subset=['message', 'agent'], inplace=True)
        return self
        
    def clean_data(self):
        # Runs the full cleaning process.:return: The cleaned pandas DataFrame.
        self.remove_duplicates()
        self.handle_missing_values()
        return self.df

class DataPreprocessor:
    # Handles preprocessing of the data.
    
    def __init__(self, df):
        # Initializes the DataPreprocessor with a DataFrame.:param df: The pandas DataFrame to preproces
        self.df = df.copy()

    def preprocess_text(self, text):
        from nltk.stem import WordNetLemmatizer
        from nltk.corpus import stopwords
        import string

        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))

        if not isinstance(text, str):
            return ""
        text = text.lower()
        from nltk.tokenize import word_tokenize
        tokens = word_tokenize(text)
        processed_tokens = [
            token for token in tokens
            if token not in stop_words and token not in string.punctuation
        ]
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in processed_tokens]
        return " ".join(lemmatized_tokens)

    def apply_text_preprocessing(self, column='message'):
        """
        Applies text preprocessing to a specified column.
        :param column: The name of the column to preprocess.
        """
        self.df[f'processed_{column}'] = self.df[column].apply(self.preprocess_text)
        return self

    def encode_categorical(self, column):
        """
        Encodes a categorical column using LabelEncoder.
        
        :param column: The name of the categorical column to encode.
        :return: A new Series with encoded labels.
        """
        encoder = LabelEncoder()
        return encoder.fit_transform(self.df[column])

    def transform_data(self):
        """
        Runs the full preprocessing pipeline.
        
        :return: The preprocessed pandas DataFrame.
        """
        self.apply_text_preprocessing()
        return self.df

if __name__ == "__main__":
    import time
    # Example usage:
    loader = DataLoader('BiztelAI_DS_Dataset_V1.json')
    df = loader.to_dataframe()
    print("Dataset loaded successfully.")
    print("Initial shape:", df.shape)

    cleaner = DataCleaner(df)
    cleaned_df = cleaner.clean_data()
    print("\nDataset cleaned.")
    print("Shape after cleaning:", cleaned_df.shape)
    
    preprocessor = DataPreprocessor(cleaned_df)
    start = time.time()
    preprocessor.apply_text_preprocessing()
    processed_df = preprocessor.df
    elapsed = time.time() - start
    print(f"\nDataset preprocessed.")
    print(f"Preprocessing time: {elapsed:.2f} seconds")
    print("Shape after preprocessing:", processed_df.shape)
    
    print("\nFirst 5 rows with processed message:")
    print(processed_df[['message', 'processed_message']].head())
    
    print("\nExample of categorical encoding for 'sentiment':")
    sentiment_encoded = preprocessor.encode_categorical('sentiment')
    print(processed_df['sentiment'].head())
    print(sentiment_encoded[:5])

    # --- Save preprocessing proof to a file ---
    proof_sample = processed_df[['message', 'processed_message']].head(10)
    with open('preprocessing_working.txt', 'w', encoding='utf-8') as f:
        f.write("--- Preprocessing Proof ---\n\n")
        f.write(f"Preprocessing time: {elapsed:.2f} seconds\n\n")
        f.write("This file shows a sample of 10 messages before and after preprocessing.\n")
        f.write("Preprocessing includes: lowercasing, tokenization, stopword and punctuation removal, and lemmatization.\n\n")
        
        for index, row in proof_sample.iterrows():
            f.write(f"--- Record {index + 1} ---\n")
            f.write(f"Original:  {row['message']}\n")
            f.write(f"Processed: {row['processed_message']}\n\n")
            
    print("\nPreprocessing proof saved to preprocessing_working.txt")

    # Final DataFrame is in processed_df
    # print("Final DataFrame Info:")
    # processed_df.info() 
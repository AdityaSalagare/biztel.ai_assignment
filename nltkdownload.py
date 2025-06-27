import nltk

def download_nltk_data():
    """
    Downloads the necessary NLTK data packages (stopwords, punkt, wordnet).
    """
    try:
        nltk.data.find('corpora/stopwords')
        print("NLTK 'stopwords' is already downloaded.")
    except LookupError:
        nltk.download('stopwords')

    try:
        nltk.data.find('tokenizers/punkt')
        print("NLTK 'punkt' is already downloaded.")
    except LookupError:
        nltk.download('punkt')

    try:
        nltk.data.find('corpora/wordnet')
        print("NLTK 'wordnet' is already downloaded.")
    except LookupError:
        nltk.download('wordnet')

if __name__ == "__main__":
    download_nltk_data()
    print("\nNLTK data check complete.")
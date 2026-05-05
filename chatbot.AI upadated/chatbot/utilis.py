try:
    import nltk
    nltk.download('punkt', quiet=True)
except ImportError:
    nltk = None

def preprocess_text(text):
    if nltk is None:
        raise ImportError("nltk is not installed. Please install it using 'pip install nltk'")
    tokens = nltk.word_tokenize(text.lower())
    return [t for t in tokens if t.isalnum()]

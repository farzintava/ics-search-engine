import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize



def tokenize(text):
    text = text.lower()
    stop_words = set(stopwords.words('english'))
    return [token for token in word_tokenize(text) if not token in stop_words and token.isascii()]
    

def lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


def process_text(text):
    tokens = tokenize(text)
    processed_tokens = lemmatize(tokens)
    return processed_tokens

def tokens_freqency(tokens):
    tf = {}
    for token in tokens:
        if token in tf:
            tf[token] += 1
        else:
            tf[token] = 1
    return tf


def create_bigram(tokens):
    bigrams = []
    for i in range(0, len(tokens)-1):
        bigrams.append(f"{tokens[i]} {tokens[i+1]}")
    return bigrams
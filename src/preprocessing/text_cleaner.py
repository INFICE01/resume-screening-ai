import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK data (run once)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    """
    Cleans input text by:
    - Lowercasing
    - Removing punctuation
    - Removing digits
    - Removing stopwords
    - Lemmatizing words
    """
    # Lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Tokenize
    tokens = nltk.word_tokenize(text)
    
    # Remove stopwords
    tokens = [word for word in tokens if word not in stop_words]
    
    # Lemmatize
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # Join back to string
    cleaned_text = ' '.join(tokens)
    
    return cleaned_text

# Example usage
if __name__ == "__main__":
    sample_text = "John Doe has 5 years of experience in Python, ML, and Data Analysis."
    print("Original Text:\n", sample_text)
    print("Cleaned Text:\n", clean_text(sample_text))

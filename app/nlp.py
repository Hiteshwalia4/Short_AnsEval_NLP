# NLP
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text)

    # Removing stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [ word for word in tokens if word.lower() not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    # Removing non-alphabetic characters
    alphabetic_tokens = [ token for token in lemmatized_tokens if token.isalpha()]

    # Joining the tokens into string
    preprocessed_text = ' '.join(alphabetic_tokens)
    return preprocessed_text

def evaluate_answer(user_answer, reference_answer):
    # Convert answer to lowercase
    answer = user_answer.lower()

    # Preprocessing of answer, and reference answer
    preprocessed_answer = preprocess_text(answer)
    preprocessed_reference_answer = preprocess_text(reference_answer)

    # Creating a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the vectorizer on the preprocessed texts
    tfidf_matrix = vectorizer.fit_transform(
        [preprocessed_answer, preprocessed_reference_answer])

    # Calculate the cosine similarity between the answer and the reference answer
    similarity = cosine_similarity(tfidf_matrix[1:2], tfidf_matrix[2:3])

    # Marks calculated
    marks = math.floor((similarity*100)/10)
    return marks

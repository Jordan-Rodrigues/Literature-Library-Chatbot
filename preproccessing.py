from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
import nltk
import pdf_utils as pdf


stop_words = set(stopwords.words('english')) # Import stopwords
lemmatizer = WordNetLemmatizer()
filtered_summaries = [] # List to hold cleaned summaries

def process_content():
    try:
        for sentence in pdf.all_content:
            filtered_sentence = []
            lemmatized_sentence = []
            sentence = sentence.lower().replace(';', '').replace(':', '').replace('(', '').replace(')', '').replace(',', '').replace('.', '').replace('-', '').replace('<', '').replace('>', '')
            words = nltk.word_tokenize(sentence) # Lower case all words and remove punctuation + splitting sentences into words

            for w in words:
                if w not in stop_words:
                    filtered_sentence.append(w) # Remove stop words

            for w in filtered_sentence:
                lemmatized_sentence.append(lemmatizer.lemmatize(w)) # Lemmatize words

            filtered_summaries.append(filtered_sentence) # Append to cleaned list

        return filtered_summaries

    except Exception as e:
        print(str(e))

process_content()

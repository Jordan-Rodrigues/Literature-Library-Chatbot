from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
from nltk.tokenize import sent_tokenize
import get_text
import nltk
import re

# Function to grab keywords, entire summary, and the first sentence of the summary
def get_summary(text):
    text = str(text)
    all_text = ''.join(text).replace(']', '').replace('[', '').replace("'", '')
    all_text = re.sub(r'\[[0-9]*\]', ' ', all_text)

    key_words = keywords(all_text, lemmatize=True, words=20).split('\n')
    summary = summarize(all_text, ratio=0.01)
    first_summary_sentence = summary.split('.')[0]

    return key_words, summary, first_summary_sentence

keywords, summary, first_summary_sentence = get_summary(get_text.all_words)

# List of keywords
print(keywords)
print('\n')
# Entire summary
print(summary)
print('\n')
# First sentence of summary
#print(first_summary_sentence)
print(get_text.number_of_pages)

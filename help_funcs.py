from collections import Counter
from math import log

import numpy as np
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer

stops = stopwords.words('russian')
morph = MorphAnalyzer()

tfidf_vectorizer = TfidfVectorizer(
    analyzer="word",  # анализировать по словам или по символам (char)
    stop_words=stops,  # передаём список стоп-слов для русского из NLTK
    ngram_range=(1, 1)
)


def lemmatize(a_text):
    a_tokens = wordpunct_tokenize(a_text)
    a_lemmatized = [morph.parse(item)[0].normal_form for item in a_tokens]
    a_lemmatized = ' '.join([token for token in a_lemmatized if token.isalpha()])
    return a_lemmatized


def get_top_tf_idf_words(tfidf_vector, feature_names, top_n):
    sorted_nzs = np.argsort(tfidf_vector.data)[:-(top_n + 1):-1]
    return feature_names[tfidf_vector.indices[sorted_nzs]]


def enumerate_words(lists_of_keywords):
    i = 0
    words_indices = {}
    for keywords in lists_of_keywords:
        for word in keywords:
            if word not in words_indices:
                words_indices[word] = i
                i += 1

    return words_indices


def create_idf(lists_of_keywords):
    count_dictionary = Counter()
    for keywords in lists_of_keywords:
        words = set(keywords)
        for word in words:
            count_dictionary[word] += 1

    idf = {}
    for word, count in count_dictionary.items():
        idf[word] = log(len(lists_of_keywords) / count)
        # your code here
    return idf


def create_tf_idf(idf, lists_of_keywords, words_indices):
    tf_idf = [[0] * len(idf) for i in range(len(lists_of_keywords))]
    for n, sentence in enumerate(lists_of_keywords):
        words_counter = Counter(sentence)
        sentence_length = len(sentence)
        for word in words_counter:
            word_index = words_indices[word]
            word_tf = words_counter[word] / sentence_length
            word_tf_idf = word_tf * idf[word]

            tf_idf[n][word_index] = word_tf_idf

    return tf_idf

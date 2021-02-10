import tensorflow as tf
import pandas as pd
import numpy as np
import nltk
from gensim import corpora
from gensim.models import word2vec
import gensim


with open(r"C:\Users\Enrique\\Desktop\chat_file.txt", 'r', encoding='utf8') as file:
    corpus = file.readlines()


def remove_stop_words(corpus):
    stop_words = ['is', 'a', 'will', 'be']
    results = []
    for text in corpus:
        tmp = text.split(' ')
        for stop_word in stop_words:
            if stop_word in tmp:
                tmp.remove(stop_word)
        results.append(" ".join(tmp))

    return results


corpus = remove_stop_words(corpus)
corpus = [k.lower() for k in corpus]

model = gensim.models.Word2Vec([corpus], min_count = 10)

def return_message(user_message):
    user_message = remove_stop_words(user_message)
    user_message = [k.lower() for k in user_message]

    return model.predict_output_word(user_message)

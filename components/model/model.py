import nltk
import pickle
import numpy as np
from nltk.stem import WordNetLemmatizer
from itertools import groupby
import tflite_runtime.interpreter as tflite
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
nltk.download("punkt")
nltk.download("wordnet")


words = pickle.load(open('./components/utils/words.pkl', 'rb'))
classes = pickle.load(open('./components/utils/classes.pkl', 'rb'))


def remove_all_consecutive(str1):
    result_str = []
    for (key, group) in groupby(str1):
        result_str.append(key)

    return ''.join(result_str)


def clean_up_sentence(sentence):
    # tokenize the pattern - splitting words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stemming every word - reducing to base form
    sentence_words = [lemmatizer.lemmatize(
        word.lower()) for word in sentence_words]
    return sentence_words
# return bag of words array: 0 or 1 for words that exist in sentence


def bag_of_words(sentence, words, show_details=True):
    # tokenizing patterns
    sentence_words = clean_up_sentence(sentence)
    # bag of words - vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % word)
    return(np.array(bag))


def model_predict(sentence):
    confidence_threshold = 0.5
    unknown_intent = "unknown_token"
    sentence = remove_all_consecutive(sentence)
    p = bag_of_words(sentence, words, show_details=False)
    interpreter = tflite.Interpreter(
        model_path="components/model/model.tflite")
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    #input_shape = input_details[0]['shape']
    input_data = np.array([p], dtype=np.float32)
    # print(len(input_data))
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_details = interpreter.get_output_details()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    results = np.squeeze(output_data)
    print(results)
    max_probability = np.argmax(results)
    print(results[max_probability])

    if results[max_probability] < confidence_threshold:
        # print(results[max_probability])
        return unknown_intent
    else:
        return classes[max_probability]

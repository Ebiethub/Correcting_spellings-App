#Library imports
import numpy as np
import pandas as pd
import streamlit as st
import cv2
import sklearn
import pickle


#Loading the Model
vocab = pickle.load(open('vocab-spellings.pkl', 'rb'))
probs = pickle.load(open('word-probability-spellings.pkl', 'rb'))


#Setting Title of App
st.title("Spelling Suggestion App")
st.write('<h3>Use this app to check spellings Suggestion</3>', unsafe_allow_html=True)

word = st.text_input('Word')

submit = st.button('Predict')
#On predict button click
if submit:

    # delete_letter()
    def delete_letter(word, verbose=False):
        delete_l = []
        split_l = []

        split_l = [(word[:i], word[i:]) for i in range(len(word))]
        delete_l = [L + R[1:] for L, R in split_l if R]

        if verbose:
            print(f"input word {word}, \nsplit_l = {split_l}, \ndelete_l = {delete_l}")  # printing implicitly.

        return delete_l

    # switch_letter()
    def switch_letter(word, verbose=False):
        def swap(c, i, j):
            c = list(c)
            c[i], c[j] = c[j], c[i]
            return ''.join(c)

        switch_l = []
        split_l = []
        split_l = [(word[:i], word[i:]) for i in range(len(word))]
        switch_l = [a + b[1] + b[0] + b[2:] for a, b in split_l if len(b) >= 2]

        if verbose:
            print(f"Input word = {word} \nsplit_l = {split_l} \nswitch_l = {switch_l}")

        return switch_l

    # replace_letter()
    def replace_letter(word, verbose=False):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        replace_l = []
        split_l = []

        split_l = [(word[:i], word[i:]) for i in range(len(word))]
        replace_l = [a + l + (b[1:] if len(b) > 1 else '') for a, b in split_l if b for l in letters]
        replace_set = set(replace_l)
        replace_set.remove(word)
        # turn the set back into a list and sort it, for easier viewing
        replace_l = sorted(list(replace_set))

        if verbose:
            print(f"Input word = {word} \nsplit_l = {split_l} \nreplace_l {replace_l}")

        return replace_l

    #  insert_letter()
    def insert_letter(word, verbose=False):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        insert_l = []
        split_l = []
        split_l = [(word[:i], word[i:]) for i in range(len(word))]
        insert_l = [a + l + b for a, b in split_l for l in letters]

        if verbose:
            print(f"Input word {word} \nsplit_l = {split_l} \ninsert_l = {insert_l}")

        return insert_l


    #  Edit one letter
    def edit_one_letter(word, allow_switches=True):

        edit_one_set = set()
        edit_one_set.update(delete_letter(word))
        if allow_switches:
            edit_one_set.update(switch_letter(word))
        edit_one_set.update(replace_letter(word))
        edit_one_set.update(insert_letter(word))

        return edit_one_set


    if word is not None:

        # Edit two letters
        def edit_two_letters(word, allow_switches=True):

            edit_two_set = set()
            edit_one = edit_one_letter(word, allow_switches=allow_switches)
            for w in edit_one:
                if w:
                    edit_two = edit_one_letter(w, allow_switches=allow_switches)
                    edit_two_set.update(edit_two)

            return edit_two_set


        # suggest spelling suggestions
        def get_corrections(word, probs, vocab, verbose=False):
            """
            Input:
                word: a user entered string to check for suggestions
                probs: a dictionary that maps each word to its probability in the corpus
                vocab: a set containing all the vocabulary
                n: number of possible word corrections you want returned in the dictionary
            Output:
                n_best: a list of tuples with the most probable n corrected words and their probabilities.
            """

            suggestions = []
            n_best = []
            # suggestions = list((word in vocab) or edit_one_letter(word).intersection(vocab) or
            #                   edit_two_letters(word).intersection(vocab))
            suggestions = list(edit_two_letters(word).intersection(vocab))
            # suggestions = list(edit_two_letters(word, False).intersection(vocab))
            n_best = [[s, probs.get(s, -1)] for s in list(reversed(suggestions))]

            if verbose:
                print("suggestions = ", suggestions)

            return n_best


        tmp_corrections = get_corrections(word, probs, vocab, verbose=False)
        for i, word_prob in enumerate(tmp_corrections):
            st.title(f"word {i}: {word_prob[0]}, probability {word_prob[1]:.6f}")






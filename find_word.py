# ----------------------------------------------------------------------------+
# Program:    	FIND WORDS 
# Description:  Find the longest words from a set of letters (french)
# Author:       Laurent FERHI
# Version:      1.3
# ----------------------------------------------------------------------------+

import pandas as pd
import unicodedata
import random
from collections import Counter 

def strip_accents(s):
    """
    Remove accents from a str
    """
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def calc_score(word):
    """
    Compare word with required letters. 
    If required letters are enough to form the word, returns the length of word. Else, returns 0
    """
    common = Counter(required_letters.upper()) & Counter(word)
    if sum(common.values()) < len(word):
        return 0
    return len(word)

if __name__ == "__main__":

    # Import corpus
    data = pd.read_fwf('liste_francais.txt', header=None)
    data.columns = ['mots']
    data.mots = data.mots.apply(lambda x: x.upper()) # Lowercase words
    data.mots = data.mots.apply(strip_accents) # remove accents
    data = data.drop_duplicates()

    # Print title and input required letters
    print('\n*** LE MOT LE PLUS LONG ***\n')
    required_letters = input('Entrer les lettres \
                             (ou 0 = lettres au hasard, ou 1 = le jeu du mot le plus long): ')

    # Choose 9 random letters
    if required_letters == '0':
        required_letters = "".join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(9)])
        print('Lettres choisies pour vous: {}'.format(required_letters))

    # Choose 9 letters (vowel or consonant)
    if required_letters == '1':
        i, letter_list = 0, []
        while i < 9:
            entry = input('Voyelle ou consonne (v/c) ?')
            if entry == 'v':
                cpu_choice = random.choice('AEIOUY')
                letter_list.append(cpu_choice)
                print('Le {}. Les lettres: {}'.format(cpu_choice, "".join(letter_list)))
                i+=1
            elif entry == 'c':
                cpu_choice = random.choice('BCDFGHJKLMNPQRSTVWXZ')
                letter_list.append(cpu_choice)
                print('Le {}. Les lettres: {}'.format(cpu_choice, "".join(letter_list)))
                i+=1
            else:
                print('Saisie erronée...')
        required_letters = "".join(letter_list)
        print('\nLettres choisies pour vous: {}'.format(required_letters))

    # Calculate score
    data['score'] = data.mots.apply(calc_score)
    number_found_words = len(data[data.score != 0])

    # Returns number of solutions
    print('\n{} mots trouvés'.format(number_found_words))

    # Returns 10 best solutions if any
    if number_found_words > 0:
        input('\nAppuyer sur une touche pour avoir la solution...')
        print('\nMots les plus long trouvés (limité aux 10 premiers):\n')
        print(data[data.score != 0].sort_values('score',ascending=False).head(10).reset_index().drop('index',axis=1))

# ----------------------------------------------------------------------------+
# Program:    	FIND WORDS 
# Description:  Find the longest words from a set of letters (french)
# Author:       Laurent FERHI
# Version:      1.1
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
    if len(common) < len(word):
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
    print('\n*** CHERCHEUR DE MOTS ***\n')
    required_letters = input('Entrer les lettres (ou 0 = lettres au hasard): ')

    # Choose 9 random letters
    if required_letters == '0':
        required_letters = "".join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(9)])
        print('Lettres choisies pour vous: {}'.format(required_letters))

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

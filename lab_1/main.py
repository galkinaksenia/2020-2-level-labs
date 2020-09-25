"""
Lab 1
A concordance extraction
"""


#data = open('data.txt', encoding='utf-8').read()
data = 'The weather is sunny, the man is happy. man man happy'
def tokenize(text):
    if type(text) != str:
        return []
    else:
        lines = text.split('\n')
        tokens = []
        for words in lines:
            words = words.split ()
            for word in words:
                word = word.lower()
                word_new = ''
                for letter in word:
                    if letter.isalnum():# or letter in "'-/"
                        word_new += letter
                if word_new != '':
                    tokens.append(word_new)
        return tokens

tokens = tokenize (data) 
"""
    Splits sentences into tokens, converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of lowercased tokens without punctuation
    e.g. text = 'The weather is sunny, the man is happy.'
    --> ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
"""


stop_words = open('stop_words.txt', encoding='utf-8').read()
stop_words = stop_words.split ()
def remove_stop_words(tokens, stop_words):
    if type (tokens) != list:
        return []
    elif type (stop_words) != list:
        return tokens
    else:
        for stop_word in stop_words:
            while stop_word in tokens:
                tokens.remove (stop_word)
        return tokens
tokens = remove_stop_words (tokens, stop_words) 
"""
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    stop_words = ['the', 'is']
    --> ['weather', 'sunny', 'man', 'happy']
"""               



def calculate_frequencies(tokens):
    if type (tokens) != list or None in tokens:
        return {}
    else:
        freq_dict = {token: tokens.count (token) for token in tokens}
        return freq_dict
freq_dict = calculate_frequencies(tokens)
"""
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
"""

def get_top_n_words(freq_dict, top_n):
    if type (freq_dict) != dict or type (top_n) != int:
        return []
    else:
        top_words = []
        #sorted_by_value = sorted(freq_dict.items(), key=sort_values, reverse = True)
        #sorted_by_value = sorted(freq_dict.items(), key=lambda kv: kv[1], reverse = True) #sort by value
        sorted_dict = {k: freq_dict[k] for k in sorted(freq_dict, key=freq_dict.get, reverse=True)}
        for key in sorted_dict:
            top_words.append (key)
        return top_words[:top_n]
top_words = get_top_n_words(freq_dict, 2)
'''        for key, value in sorted (freq_dict.items(), key = freq_dict.get, reverse = True):
            top_words.append (key)
        return top_words[:top_n-1]
'''
'''         if top_words == []:
                top_words.append (key)
            else:
                for word in top_words:
                    if value > freq_dict[word]:
                        top_words = [key] + top_words
                    else:
                        top_words.append (key)
    return top_words[:top_n-1]'''
"""
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words to return
    :return: a list of the most common words
    e.g. tokens = ['weather', 'sunny', 'man', 'happy', 'and', 'dog', 'happy']
    top_n = 1
    --> ['happy']
"""


def get_concordance(tokens, word, left_context_size, right_context_size):
    concordance = []
    if type(tokens) != list or type(word) != str: # or word not in tokens
        return []
    elif type(left_context_size) != int or type(right_context_size) != int:
        return []
    elif type(left_context_size) == int and type(right_context_size) == int and left_context_size < 1 and right_context_size < 1:
        return []
    elif right_context_size < 1 and left_context_size >= 1:
        for number, token in enumerate (tokens):
            context = []
            if token == word:
                left_size = left_context_size
                while left_size != 0:
                    if number - left_size >= 0:
                        context.append (tokens[number-left_size])
                    left_size -= 1
                context.append (token)
            if context != []:
                concordance.append (context)
    elif right_context_size >= 1 and left_context_size < 1:
        for number, token in enumerate (tokens):
            context = []
            if token == word:
                context = [token]
                iterations = 1
                right_size = right_context_size
                while right_size != 0:
                    if len(tokens) > number + iterations:
                        context.append (tokens[number+iterations])
                    right_size -= 1
                    iterations += 1
            if context != []:
                concordance.append (context)
    elif right_context_size >= 1 and left_context_size >= 1:
        for number, token in enumerate (tokens):
            context = []
            if token == word:
                iterations = 1
                left_size = left_context_size
                right_size = right_context_size
                while left_size != 0:
                    if number - left_size >= 0:
                        context.append (tokens[number-left_size])
                    left_size -= 1
                context.append (token)
                while right_size != 0:
                    if len(tokens) > number + iterations:
                        context.append (tokens[number+iterations])
                    right_size -= 1
                    iterations += 1
            if context != []:
                concordance.append (context)
    return concordance
                    
"""
    Gets a concordance of a word
    A concordance is a listing of each occurrence of a word in a text,
    presented with the words surrounding it
    :param tokens: a list of tokens
    :param word: a word-base for a concordance
    :param left_context_size: the number of words in the left context
    :param right_context_size: the number of words in the right context
    :return: a concordance
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
    word = 'happy'
    left_context_size = 2
    right_context_size = 3
    --> [['man', 'is', 'happy', 'the', 'dog', 'is'], ['dog', 'is', 'happy', 'but', 'the', 'cat']]
    """


def get_adjacent_words(tokens: list, word: str, left_n: int, right_n: int) -> list:
    """
    Gets adjacent words from the left and right context
    :param tokens: a list of tokens
    :param word: a word-base for the search
    :param left_n: the distance between a word and an adjacent one in the left context
    :param right_n: the distance between a word and an adjacent one in the right context
    :return: a list of adjacent words
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
    word = 'happy'
    left_n = 2
    right_n = 3
    --> [['man', 'is'], ['dog, 'cat']]
    """
    pass


def read_from_file(path_to_file: str) -> str:
    """
    Opens the file and reads its content
    :return: the initial text in string format
    """
    with open(path_to_file, 'r', encoding='utf-8') as fs:
        data = fs.read()

    return data


def write_to_file(path_to_file: str, content: list):
    """
    Writes the result in a file
    """
    pass


def sort_concordance(tokens: list, word: str, left_context_size: int, right_context_size: int, left_sort: bool) -> list:
    """
    Gets a concordance of a word and sorts it by either left or right context
    :param tokens: a list of tokens
    :param word: a word-base for a concordance
    :param left_context_size: the number of words in the left context
    :param right_context_size: the number of words in the right context
    :param left_sort: if True, sort by the left context, False – by the right context
    :return: a concordance
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
    word = 'happy'
    left_context_size = 2
    right_context_size = 3
    left_sort = True
    --> [['dog', 'is', 'happy', 'but', 'the', 'cat'], ['man', 'is', 'happy', 'the', 'dog', 'is']]
    """
    pass

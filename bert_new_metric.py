import nltk
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
import pandas as pd
from rouge_metric import PyRouge
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import web1 as web
stopwords = stopwords.words('english')
#filter out the single words
def text_filter(row_text):
    return len(str(row_text).split(' ')) > 1

#filter out the symbol in text
def char_filter(row_char):
    available_char = [',', ' ', ';', '.']
    return row_char.isalnum() or row_char in available_char

#clean text
def text_modifier(half_row_text):
    #modify ',' back
    with_comma = str(half_row_text).strip().replace('||', ',')
    #clean non alpha/number char
    without_symbol = ''.join([character for character in with_comma if char_filter(character)])
    #clean all the '.' at the end
    if without_symbol[-1] == '.':
        end_index = len(without_symbol) - 1
        try:
            for char in without_symbol[-2::-1]:
                if char == '.':
                    end_index -= 1
                else:
                    break
        except:
            end_index = end_index
        return without_symbol[:end_index]
    return without_symbol

def clean_word(word):
    cleaned = [element for element in word if element.isalnum()]
    return "".join(cleaned)

#calculate summary score with new metric, count all the appearance of words and
#storage these appearance (score) as a dict. Then calculate the score of summary
#by add up the scores of words in dict, the higher the total score is, the closer
#to the original texts.  
def calculate_score(summary, reference):
    #deal with url with empty summary
    if type(summary) != str:
        return 0
    #collect the scores of words in a dict
    words_dict = {}
    for fragment in reference:
        words = fragment.strip().split()
        #print(words)
        for word in words:
            if word not in list(stopwords):
                to_add = clean_word(word)
                if to_add.lower() not in words_dict:
                    words_dict[to_add.lower()] = 1
                else:
                    words_dict[to_add.lower()] += 1

    #calcualte the score of summary
    score = 0
    sentences = summary.split('.')
    
    def get_score(word):
        try:
            return words_dict[clean_word(word).lower()]
        except:
            contained = ''
            lst = list(words_dict.keys())
            for choice in lst:
                if clean_word(word).lower() in choice:
                    contained = choice
                    break
            if len(contained) == 0:
                return 0
            else:
                return words_dict[clean_word(contained).lower()]

    for sentence in sentences:
        words = sentence.strip().split()
        score += sum([get_score(word) for word in words 
            if word not in list(stopwords)])
        
    try:
        return score/sum(words_dict.values())
    except:
        return 0

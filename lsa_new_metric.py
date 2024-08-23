from lsa_summarizer import LsaSummarizer
import nltk
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
import pandas as pd
from rouge_metric import PyRouge
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

summarizer = LsaSummarizer()
stopwords = stopwords.words('english')
summarizer.stop_words = stopwords

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

#calcualte score of summary by new metric, sort all words in order based on 
#appearance, assign them with their appearance as scores, then for each sentence,
#calculate the scores of whole sentence with all words concluded. Sort again,
#we can get a list from sentence with most words of most appearance, if our 
#summary is at the first 10% position of the list, then this summary could be
#good
def calculate_score(summary, reference):
    #put all words in a dict with appearance
    words_dict = {}
    for fragment in reference:
        words = fragment.split()
        for word in words:
            if word.lower() not in list(stopwords):
                to_add = clean_word(word)
                if to_add.lower() not in words_dict:
                    words_dict[to_add.lower()] = 1
                else:
                    words_dict[to_add.lower()] += 1

    #put all sentence in a dict with their scores
    all_scores = {}
    for sentence in reference:
        words = sentence.split()
        if sentence not in all_scores:
            all_scores[sentence] = sum([words_dict[clean_word(word).lower()] 
                for word in words if word.lower() not in list(stopwords)])
        else:
            all_scores[sentence] += sum([words_dict[clean_word(word).lower()] 
                for word in words if word.lower() not in list(stopwords)])
    #turn dict into tuple with each pair in form of (appearance, sentence)
    sentence_scores = [(tup[1], tup[0]) for tup in list(tuple(all_scores.items()))]
    #sort tuple list so that the sentence with most important words at the start
    sentence_scores.sort(reverse = True)
    #change back into dict
    ordered_sentence_scores_dict = {tup[1]:tup[0] for tup in sentence_scores}
    #find the position in this ordered list, return the percent of this position
    try:
        score1 = (list(ordered_sentence_scores_dict.keys())
            .index(summary[0]) + 1) / len(ordered_sentence_scores_dict)
        score2 = (list(ordered_sentence_scores_dict.keys())
            .index(summary[1]) + 1) / len(ordered_sentence_scores_dict)
        return (score1 + score2) / 2
    except:
        return 0

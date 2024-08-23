#from lsa_summarizer import LsaSummarizer
import nltk
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
import pandas as pd
from rouge_metric import PyRouge
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import web1 as web
from summarizer import Summarizer
model = Summarizer()

# summarizer = LsaSummarizer()
# stopwords = stopwords.words()
# summarizer.stop_words = stopwords
detail_df = pd.read_csv("url100_detail.csv")

def text_filter(row_text):
    return len(str(row_text).split(' ')) > 1

def char_filter(row_char):
    available_char = [',', ' ', ';', '.']
    return row_char.isalnum() or row_char in available_char

def text_modifier(half_row_text):
    #modify ',' back
    with_comma = str(half_row_text).strip().replace('||', ',')
    #clean non alpha/number char
    without_symbol = ''.join([character for character in with_comma if char_filter(character)])
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


url = 'http://davisproductsco.com/'
url_df = detail_df[detail_df['url'] == url]
contents = url_df['texts'].tolist()
#result = web.scrape(url)
text_lst = [text_modifier(content) for content in contents
    if text_filter(content)]
text = '. '.join(text_lst)
    
summary = model(text, num_sentences = 2)
print(summary)

# summary = [' '.join(list(summary))]
# reference = [text]

def calculate_score(summary, reference):
    #if math.isnan(summary):
    if type(summary) != str:
        return 0
    words_dict = {}
    for fragment in reference:
        words = fragment.split()
        for word in words:
            if word.lower() not in words_dict:
                words_dict[word.lower()] = 1
            else:
                words_dict[word.lower()] += 1

    # #turn dict into tuple with each pair in form of (appearance, word)
    # words_dict_tuple_lst = [(tup[1], tup[0]) for tup in list(tuple(words_dict.items()))]
    # #sort tuple list so that the word with most appearance at the start
    # words_dict_tuple_lst.sort(reverse = True)
    # ordered_words_appearance = words_dict_tuple_lst

    # if len(ordered_words_appearance) <= 10:
    #     return ordered_words_appearance[:len(ordered_words_appearance)//2]
    # return ordered_words_appearance[:10]
    score = 0
    sentences = summary.split('.')
    for sentence in sentences:
        words = sentence.strip().split()
        score += sum([words_dict[word.lower()] if word.lower() in words_dict else 0 for word in words])
    try:
        return score/sum(words_dict.values())
    except:
        return 0
    #turn dict into tuple with each pair in form of (appearance, sentence)
    sentence_scores = [(tup[1], tup[0]) for tup in list(tuple(all_scores.items()))]
    #sort tuple list so that the word with most appearance at the start
    sentence_scores.sort(reverse = True)
    ordered_sentence_scores_dict = {tup[1]:tup[0] for tup in sentence_scores}
    try:
        score1 = (list(ordered_sentence_scores_dict.keys())
            .index(summary[0])+1)/len(ordered_sentence_scores_dict)
        score2 = (list(ordered_sentence_scores_dict.keys())
            .index(summary[1])+1)/len(ordered_sentence_scores_dict)
        return (score1 + score2) / 2
    #return ordered_sentence_scores_dict
    except:
        return 0

result = calculate_score(summary, sent_tokenize(text))
print(result)



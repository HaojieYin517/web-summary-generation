from lsa_summarizer import LsaSummarizer
import nltk
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
import pandas as pd
from nltk.corpus import stopwords
import lsa_new_metric
import bert_new_metric
import summarization_Bert as Bert
from nltk.tokenize import sent_tokenize, word_tokenize

def text_filter(row_text):
    return len(str(row_text).split(' ')) > 1

def char_filter(row_char):
    available_char = [',', ' ', ';', '.']
    return row_char.isalnum() or row_char in available_char

def text_modifier(half_row_text):
    with_comma = str(half_row_text).strip().replace('||', ',')
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

summarizer = LsaSummarizer()
stopwords = stopwords.words('english')
summarizer.stop_words = stopwords

#'url100_detail.csv', 'url100_basic_info.csv'
def summarize(detail_file, basic_file):
    detail_df = pd.read_csv(detail_file)
    basic_df =pd.read_csv(basic_file)

    url_lst = basic_df['url'].tolist()
    summary_lst = []
    summary_score_new_metric = []
    for url in url_lst:
        print(url)
        url_df = detail_df[detail_df['url']==url] 
        contents = url_df['texts'].tolist()
        text_lst = [text_modifier(content) for content in contents 
            if text_filter(content)]
        text = '. '.join(text_lst)
        
        lsa_summary =summarizer(text, 2)
        bert_summary = Bert.model(text, num_sentences = 2)
        bert_score_new_metric = bert_new_metric.calculate_score(bert_summary, sent_tokenize(text))
        #
        lsa_score_new_metric = lsa_new_metric.calculate_score(lsa_summary, sent_tokenize(text))
        
        if lsa_score_new_metric <= 0.09:
            if bert_score_new_metric >= 0.5:
                summary = bert_summary
            else:
                summary = " ".join(lsa_summary)
        else:
            summary = bert_summary
        
        
        
        summary_lst.append(summary)
        # summary_score_new_metric.append(score_new_metric)

    basic_df['summary'] = summary_lst
    #basic_df['summary_score_new_metric'] = summary_score_new_metric
    #33-':' included, 32-':'excluded
    basic_df.to_csv('output_new2.csv', index=False)

summarize('url100_detail.csv', 'url100_basic_info.csv')
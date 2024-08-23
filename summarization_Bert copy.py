#from summarizer import Summarizer
#model = Summarizer()
import pandas as pd
import bert_new_metric as new_metric
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
from rouge_metric import PyRouge
from summarizer import Summarizer
model = Summarizer()



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
        text_lst = [new_metric.text_modifier(content) for content in contents 
            if new_metric.text_filter(content)]
        text = '. '.join(text_lst)
        
        summary = model(text, num_sentences = 2)
        score_new_metric = new_metric.calculate_score(summary, sent_tokenize(text))
        summary_lst.append(summary)
        summary_score_new_metric.append(score_new_metric)
        # try:
        #     summarizer = LsaSummarizer()
        #     stopwords = stopwords.words()
        #     summarizer.stop_words = stopwords
        #     summary =summarizer(text, 3)
        #     summary_lst.append(" ".join(summary))
        # except:
        #     summary_lst.append('none')

    basic_df['summary'] = summary_lst
    basic_df['summary_score_new_metric'] = summary_score_new_metric
    basic_df.to_csv('output_bert_new_metric.csv', index=False)

rouge = PyRouge(rouge_n=(1), rouge_l=True, rouge_w=True,
    rouge_w_weight=1.2, rouge_s=True, rouge_su=False, skip_gap=4)
#'output_bert_new_metric.csv'
def calculate_metric(summary_file, detail_file):
    detail_df = pd.read_csv(detail_file)
    basic_df =pd.read_csv(summary_file)
    summary_score_new_metric = []
    rouge_1 = []
    rouge_w = []
    rouge_l = []
    rouge_s = []


    for i in range(basic_df.shape[0]):
        print(basic_df.iloc[i]['url'])
        
        url_df = detail_df[detail_df['url']==basic_df.iloc[i]['url']] 
        contents = url_df['texts'].tolist()
        text_lst = [new_metric.text_modifier(content) for content in contents 
            if new_metric.text_filter(content)]
        text = '. '.join(text_lst)
        print(basic_df.iloc[i]['summary'])

        score_new_metric = new_metric.calculate_score(basic_df.iloc[i]['summary'], sent_tokenize(text))
        summary_score_new_metric.append(score_new_metric)

        if type(basic_df.iloc[i]['summary']) != str:
            rouge_1.append(0)
            rouge_l.append(0)
            rouge_w.append(0)
            rouge_s.append(0)
            continue
        
        scores = rouge.evaluate([basic_df.iloc[i]['summary']], [text])
        rouge_1.append(scores['rouge-1'])
        rouge_l.append(scores['rouge-l'])
        rouge_w.append(scores['rouge-w-1.2'])
        rouge_s.append(scores['rouge-s4'])

    basic_df['summary_score_new_metric'] = summary_score_new_metric
    basic_df['rouge_1'] = rouge_1
    basic_df['rouge_w'] = rouge_w
    basic_df['rouge_l'] = rouge_l
    basic_df['rouge_s'] = rouge_s
    basic_df.to_csv('output_bert_new_metric.csv', index=False)



#summarize('url100_detail.csv', 'url100_basic_info.csv')
#calculate_metric('output_bert_new_metric.csv', 'url100_detail.csv')
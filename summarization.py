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

summarizer = LsaSummarizer()
stopwords = stopwords.words('english')
summarizer.stop_words = stopwords

#create summary based on the score of lsa and bert metric scores
#'url100_detail.csv', 'url100_basic_info.csv'
def summarize(detail_file, basic_file):
    #basic set up
    detail_df = pd.read_csv(detail_file)
    basic_df =pd.read_csv(basic_file)
    url_lst = basic_df['url'].tolist()
    summary_lst = []

    #create summary url by url
    for url in url_lst:
        #for tracing summarization
        print(url)
        #retrieve the basic info of url
        url_df = detail_df[detail_df['url']==url] 
        #retrieve the texts for next summarizing
        contents = url_df['texts'].tolist()
        text_lst = [lsa_new_metric.text_modifier(content) for content in contents 
            if lsa_new_metric.text_filter(content)]
        text = '. '.join(text_lst)
        
        #create summary by lsa and bert, calculate their scores
        lsa_summary = summarizer(text, 2)
        bert_summary = Bert.model(text, num_sentences = 2)
        bert_score_new_metric = bert_new_metric.calculate_score(bert_summary, sent_tokenize(text))
        lsa_score_new_metric = lsa_new_metric.calculate_score(lsa_summary, sent_tokenize(text))
        
        #rules to select summary, required next improvement!
        if lsa_score_new_metric <= 0.35:
            if bert_score_new_metric >= 0.18:
                summary = bert_summary
            else:
                summary = " ".join(lsa_summary)
        else:
            summary = bert_summary
        
        #add the winner into summary list
        summary_lst.append(summary)

    #add summary col into original basic_info csv, output as a new csv
    basic_df['summary'] = summary_lst
    basic_df.to_csv('output_book1.csv', index=False)

#summarize('url100_detail.csv', 'url100_basic_info.csv')
summarize('url1_detail.csv', 'url1_basic_info.csv')
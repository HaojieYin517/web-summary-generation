import csv
import pandas as pd
import web1

# scrape_result = web1.scrape(web1.URL3)
# url_data = scrape_result[1:]

#calculate which element has most in this web, text, link, or other
def max_len(url_data):
    return max([len(lst) for lst in url_data])

#decide the data in each row of csv form
def retrieve_data(data_lst, index):
    data = []
    #3 without link words
    for i in range(3):
        try:
            data.append(data_lst[i][index])
        except:
            data.append(None)
    return data

#write the data into csv file in either basic info way or detailed way
def write_to_csv(url_list, infile):
    detail_outfile = infile[:-4]+'_detail'+infile[-4:]
    basic_info_outfile = infile[:-4]+'_basic_info'+infile[-4:]
    #write detailed report with all text, links info
    #columns in csv file
    #detail_header = ['url', 'texts', 'links', 'links_word', 'img_url']
    detail_header = ['url', 'texts', 'links', 'img_url']
    basic_info_header = ['url', 'title', 'description', 'keywords', 'contact_info']

    with open(detail_outfile, 'a', encoding='UTF8', newline='') as detail_file:
        with open(basic_info_outfile, 'a', encoding='UTF8', newline='') as basic_info_file:
            detail_writer = csv.DictWriter(detail_file, fieldnames = detail_header)
            basic_info_writer = csv.DictWriter(basic_info_file, fieldnames = basic_info_header)

            # write the header
            detail_writer.writeheader()
            basic_info_writer.writeheader()

            #write the data for each url
            for url in url_list:
                #scrape the data
                scrape_result = web1.scrape(url)

                #deal with non-connection web
                if len(scrape_result) == 0:
                    continue

                url_data = scrape_result[1:]
                basic_info = scrape_result[0]

                # write rows of available web
                for i in range(max_len(url_data)):
                    retrieved_data = retrieve_data(url_data, i)
                    detail_writer.writerow({
                        'url': url, 
                        'texts':retrieved_data[0], 
                        'links':retrieved_data[1], 
                        #'links_word':retrieved_data[2], 
                        'img_url':retrieved_data[2]
                    })

                basic_info.update({'url':url})
                basic_info_writer.writerow(basic_info)


#main function to get all data from a csv file with links, then record all the 
#data into a new csv file
def collect_data(filepath):
    df = pd.read_csv(filepath)  
    url_lst = df['Url'].tolist()
    # write_to_csv(url_lst[:10], outfile)
    write_to_csv(url_lst, filepath)
    return True


#test
test_file_1 ='url100.csv'
test_file_2 = 'url1.csv'
collect_data(test_file_2)
#result = (web1.search_links('http://davisproductsco.com/', web1.get_content('http://davisproductsco.com/'))()[0])
#print(result)
# df = pd.read_csv('url100_detail.csv')
# print(df)
# url2_df = df[df['url']=='http://eatatruperts.com/'] 
# contents = url2_df['texts'].tolist()

# with open ('url2.txt', 'a') as f:
#     for word in contents:
#         try:         
#             f.write(word + '.\n')
#         except:
#             continue
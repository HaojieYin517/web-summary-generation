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
    for i in range(4):
        try:
            data.append(data_lst[i][index])
        except:
            data.append(None)
    return data

#write the data into csv file in either basic info way or detailed way
def write_to_csv(url_list, outfile, be_detailed = True):

    #write detailed report with all text, links info
    if be_detailed:
        #columns in csv file
        header = ['url', 'texts', 'links', 'links_word', 'img_url']
        with open(outfile, 'a', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames = header)

            # write the header
            writer.writeheader()

            #write the data for each url
            for url in url_list:
                #scrape the data
                scrape_result = web1.scrape(url)

                #deal with non-connection web
                if len(scrape_result) == 0:
                    continue

                url_data = scrape_result[1:]

                # write rows of available web
                for i in range(max_len(url_data)):
                    retrieved_data = retrieve_data(url_data, i)
                    writer.writerow({
                        'url': url, 
                        'texts':retrieved_data[0], 
                        'links':retrieved_data[1], 
                        'links_word':retrieved_data[2], 
                        'img_url':retrieved_data[3]
                    })
    #write the basic info of this web
    else:
        #columns in csv file
        header = ['url', 'title', 'description', 'keywords', 'contact_info']
        with open(outfile, 'a', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames = header)

            # write the header
            writer.writeheader()

            #write the data for each url
            for url in url_list:
                #scrape the data
                scrape_result = web1.scrape(url)

                #deal with non-connection web
                if len(scrape_result) == 0:
                    continue

                basic_info = scrape_result[0]
                basic_info.update({'url':url, 'contact_info':'0000000000'})
                writer.writerow(basic_info)


#main function to get all data from a csv file with links, then record all the 
#data into a new csv file
def collect_data(filepath):
    detail_outfile = filepath[:-4]+'_detail'+filepath[-4:]
    basic_info_outfile = filepath[:-4]+'_basic_info'+filepath[-4:]
    df = pd.read_csv(filepath)  
    url_lst = df['Url'].tolist()
    # write_to_csv(url_lst[:10], outfile)
    write_to_csv(url_lst, detail_outfile)
    write_to_csv(url_lst, basic_info_outfile, be_detailed= False)
    return True


#test
test_file_1 ='url100.csv'
collect_data(test_file_1)
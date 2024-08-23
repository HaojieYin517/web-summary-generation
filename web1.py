import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests_html import HTMLSession
session = HTMLSession()

#check if we can scrape the web
def can_fetch(content):
    fetch_limit = content.find_all("meta", content = "noarchive")
    if len(fetch_limit) != 0:
        return False
    return True

#java script web
def get_content_java(link):
    r = session.get(link)
    r.html.render()
    return BeautifulSoup(r.content, "html.parser", from_encoding="iso-8859-1")

#create a beautifulsoup of target web
def get_content(link):
    try:
        page = requests.get(link, headers={'User-Agent': 'XYZ/3.0'})
    except:
        return None
    #page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
    #print(page.text)
    # with open('saving.html', 'wb+') as f:
    #     f.write(page.content)
    return BeautifulSoup(page.content, "html.parser", from_encoding="iso-8859-1")

#clean comma in texts
def clean_comma(input):
    if type(input) == str:
        return input.replace(',','||')
    if type(input) == list:
        divided = []
        for text in input:
            divided += text.split(',')
        return divided
    return input

#search title, keyword, and description if possible
def search_header(content):
    basic_info = {}
    header = content.find('head')
    
    #find title
    if content.title != None:
        basic_info['title'] = clean_comma(content.title.text.strip())
    else:
        basic_info['title'] = None

    #find description & keywords
    infos= header.find_all("meta")
    description = None
    keywords = None
    for info in infos:
        try:
            if "descri" in info.get("name").lower():
                description = clean_comma(info.get('content'))
            if "keyword" in info.get('name').lower():
                keywords = clean_comma(info.get('content'))
        except:
            continue
    basic_info['description'] = description
    basic_info['keywords'] = keywords

    return basic_info

# search all links in the web
def search_links(url, content):
    all_links_object = content.find_all("a") + content.find_all('link')
    #print(all_links)
    links = []
    link_words = []
    for link_object in all_links_object:
        #link_url = link["href"]
        link = link_object.get('href')
        if link == None:
            continue
        #retrieve the words in link
        #link_words += [clean_comma(word) for word in list(link.split('/')) if word not in link_words or word != '']
        
        #directly add the workable link and modify the incomplete links into 
        #complete ones
        if len(link) == 0 or ',' in link:
            continue
        if 'www' in link or 'http' in link:
            links.append(link)
        elif link[0] == '/' and url[-1] == '/':
            links.append(url[:-1]+link)
        elif link[0] != '/' and url[-1] != '/':
            links.append(url+'/'+link)
        else:
            links.append(url+link)

    def link_result():
        return [list(set(links)), list(set(link_words))]

    return link_result
    #return links

#search the links of all images
def search_img(url, content):
    all_imgs_object = content.find_all("img")
    #print(all_imgs)
    links = []
    for img_object in all_imgs_object:
        link = img_object.get('src')
        if link == None or ',' in link:
            continue
        if 'www' in link:
            links.append(link)
        else:
            links.append(url+link)
    
    return list(set(links))
    #return links

#search all the texts 
def search_text(content):
    texts = [clean_comma(text) for text in content.stripped_strings]
    return texts

def search_contact(texts):
        
    for i in range(len(texts) - 1, len(texts)//2 ,-1):
        if 'phone' in texts[i].lower():
            if len([character for character in texts[i] if character.isdigit()]) >= 6:
                return texts[i][texts[i].lower().find('phone'):]
            if len([character for character in texts[i+1] if character.isdigit()]) >= 6:
                return texts[i+1]
        
    return "00000000"

#main scrape function
def scrape(url):
    result = []
    content = get_content(url)
    if content == None:
        return result
    if can_fetch:
        frameset = content.find_all("frame")
        if len(frameset) != 0:
            for frame in frameset:
                try:
                    scrape(frame.get('src'))
                except:
                    continue

        #search text & contact info
        texts = search_text(content)

        #search title, keywords, or description
        basic_info = search_header(content)
        basic_info.update({'contact_info': search_contact(texts)})
        result.append(basic_info)
        #print(basic_info)
        #print('################################')

        #record texts
        result.append(texts)
        #print(f'text: {texts}')
        #print('################################')

        #search links
        links_result = search_links(url, content)()
        links = links_result[0]
        #link_words = links_result[1]
        result.append(links)
        #result.append(link_words)
        #print(f'link: {links}')
        #print(f'link_words: {link_words}')
        #print('################################')

        #search imgs
        images = search_img(url, content)
        result.append(images)
        #print(f'image: {images}')
        
    return result


#web with frame and empty web page
URL1 = 'http://az-property-plus.com/'


URL2 = 'https://davisproductsco.com/'
URL3 = 'http://digitizerzone.com'
URL4 = 'https://www.eatatruperts.com/'
URL5 = 'https://www.myshedplans.com/'
URL5 = 'http://eliaslandscapingservices.com/'
URL6 = 'http://heartburnhomeremedies.net'

#try this
soup = get_content("https://www.jeansrs.com/tabletop/dinnerware/melamine/melamine-plates.html")
result = scrape("https://www.jeansrs.com/tabletop/dinnerware/melamine/melamine-plates.html")
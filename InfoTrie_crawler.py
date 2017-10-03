# -*- coding: utf-8 -*-

import sys
import requests
import json
import bs4
import datetime
import time, threading

reload(sys)  
sys.setdefaultencoding('utf8')

# process the html content
def process(content, last_request_datetime):
    soup = bs4.BeautifulSoup(content, "html.parser")

    # All news articles are rows of table
    table = soup.find('table')
    tbody = table.find('tbody')
    articleRows = tbody.find_all('tr')
    result = []

    for articleRow in articleRows:
        article_datetime = articleDetail.find('span').text.strip()
        formatted_datetime = datetime.datetime.strptime(article_datetime, '%d-%m-%Y (%H:%M:%S)')
        formatted_datetime_str = formatted_datetime.strftime('%Y-%m-%d %H:%M:%S')
        
        # check if the article is latest
        if formatted_datetime_str > last_request_datetime:
            # parse article details
            articleDetail = articleRow.find('a', class_="modalLink")
            article_brief = articleDetail.get('data-teaser').strip()
            article_link = articleDetail.get('data-link').strip()
            article_title = articleDetail.find('b').text.strip()

            result.append({'title': article_title, 'link': article_link, 'detail': article_brief, 'datetime': formatted_datetime_str})
    return result

# Send POST request to FinSents web page and fetch latest news articles
def requestInfoTrie(last_request_datetime):
    url = "http://www.finsents.com/Home/GetDashBoardData"
    headers = {
        'Cache-Control' : 'no-cache',
        # Give in a session id to avoid login
        'Cookie': '_ga=GA1.2.785060912.1506675561; __zlcmid=ikgmaNjfkbzBCI; ASP.NET_SessionId=bizrcrv5tqfeyg140xczwcur; __RequestVerificationToken=2u1HuP_3T87lbwmHpJBWRMyDb9pVfpiU1sWsfW2zLaGeRudUHLORgZs2BwT4jfXzd7S6PyT2VIK8Tj-Fd0Y7nGjj-ZkXivBftcQnlpCKMfQ1; Platform=web; fsweb.auth=B1ABB9C767347B1F37E28498867E9E421B88EA4A2DA44726D61ABFFE443B3117F3B3FD93CDB075F91621CD62450D652FC68B4F8803AC8248C08DBF27883F657C840CB76707B99064A21C082B60AF43010B320231511CBD83FEBF254F185ACDD1D919D2F42F3A5965C7DE749FD3CB00FACD16DDC3FBAC9884BB3277518C642FC0',
        'Connection' : 'keep-alive'
    }
    # log request
    print "Request starts at " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # POST request paylod
    # param allows to fetch all types of articles
    payload = {'source': 'NewsArticles', 'param': 'app=finsents&q=( forex OR fx OR equities OR market OR stocks OR investors OR commodities OR mining OR ore OR futures OR agriculture OR wti OR grains OR corn OR soybean OR merger OR acquisition OR ipo OR dividend OR tech OR technology OR earning ) NOT ( sport OR football OR soccer OR basketball OR fc OR athletics OR food OR chef OR entertainment OR celebrity OR series OR tv OR wildlife OR animal )'}
    r = requests.post(url, data=payload, verify=False, headers = headers)

    try:
        # process fetched result
        fetched_articles = process(r.text.encode('utf-8'), last_request_datetime)

        # Append lastest articles to file
        append_file = open('InfoTrie_latest_news.txt' , 'a')
        for article in fetched_articles:
            # Update lastest datetime
            if article["datetime"] > last_request_datetime:
                last_request_datetime = article["datetime"]
            append_file.write(str(article) + '\n')

        # log result
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + str(len(fetched_articles)) + " articles fetched after " + last_request_datetime)
        return last_request_datetime
    # log exception
    except Exception, e:
        print Exception
        print str(e)

# Give empty initial value
last_request_datetime = '0000-00-00 00:00:00'

# Run the program every 10 seconds
while True:
    last_request_datetime = requestInfoTrie(last_request_datetime)
    time.sleep(10)

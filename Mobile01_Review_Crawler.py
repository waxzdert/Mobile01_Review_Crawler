import warnings
warnings.filterwarnings('ignore')
import sys
import re
import time
import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
from multiprocessing import Pool
from datetime import datetime

crawl_time_delta = 0
temp_time_delta = int(input('請輸入要幾小時內的回覆\n'))
crawl_time_delta = temp_time_delta*60*60
today = datetime.now()

def GetPageContent(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    res = requests.get(url, headers=headers)
    content = BeautifulSoup(res.text)
    return content

def Parse(content):
    #soup = GetPageContent('https://www.mobile01.com/' + url)
    #origin = soup.find('div', {'class':'single-post-content'}) # 文章內文在 <div class="single-post-content"> 底下
    origin = content
    if origin:
        content = str(origin)
        # replace <br>, <br\> and '\n' with a whitespace########
        content = re.sub("<br\s*>", " ", content, flags=re.I)  #
        content = re.sub("<br\s*/>", " ", content, flags=re.I) #
        content = re.sub("\n+", " ", content, flags=re.I)      #
        ########################################################
        # remove hyperlink
        content = re.sub("<a\s+[^<>]+>(?P<aContent>[^<>]+?)</a>", "\g<aContent>", content, flags=re.I)
        content = BeautifulSoup(content)
        content = ' '.join(content.text.lstrip().rstrip().split())
    else:
        content = 'None'

    return content

def GetPageReviews(url):
    All_page_Contents = GetPageContent(url)
    Review_list = All_page_Contents.find_all('div',{'class':'l-articlePage'})
    
    Main_post_week = datetime.strptime((Review_list[0].find('span',{'class':'o-fNotes o-fSubMini'})).text[0:10], '%Y-%m-%d')
    main_week_num = Main_post_week.date().isocalendar()[1]

    resp = list()
    
    for i in range(len(Review_list)):

        Reviews_date = datetime.strptime((Review_list[i].find('span',{'class':'o-fNotes o-fSubMini'})).text[0:19], '%Y-%m-%d %H:%M')
        # print(Reviews_date)
        time_delta = today - Reviews_date
        review_delta = int(time_delta.total_seconds())
        #print(review_delta)
        #print('%f,%d'% (review_delta, crawl_time_delta))
        if(Review_list[i].find('article') == None):
            pass
        elif(review_delta > crawl_time_delta):
            pass
        else:
            date = datetime.strptime((Review_list[i].find('span',{'class':'o-fNotes o-fSubMini'})).text[0:10], '%Y-%m-%d')
            time = datetime.strptime((Review_list[i].find('span',{'class':'o-fNotes o-fSubMini'})).text[11:19], '%H:%M')
            topic = All_page_Contents.find('h1',{'class':'t2'}).text    
            review = Parse(Review_list[i].find('article').text) 
            id = Parse(Review_list[i].find('a',{'class':'c-link c-link--gn u-ellipsis'}))
            post_week_num = date.date().isocalendar()[1]

            if(main_week_num < post_week_num):
                post_week = ''
            else:
                post_week = 'V'

            resp.append({
                'post_week':post_week,
                'date':date,
                'time':time,
                'topic':topic,
                'review':review,
                'id':id,
                'url':url
            })
            #print(resp)
        
    return resp

def Save2Excel(posts):
    post_week = [entry['post_week'] for entry in posts]
    topics = [entry['topic'] for entry in posts]
    links = [entry['url'] for entry in posts]
    dates = [entry['date'] for entry in posts]
    times = [entry['time'] for entry in posts]
    authors = [entry['id'] for entry in posts]
    contents = [entry['review'] for entry in posts]
    df = DataFrame({
        '發文周':post_week,
        '主題':topics,
        'URL':links,
        '日期': dates,
        '時間':times,
        'id':authors,
        '留言': contents
        })
    
    output_name = input('請輸入輸出檔名\n')
    
    final_name = output_name + '.xlsx'
    
    df.to_excel(final_name, sheet_name='sheet1', index=False, columns=['發文周','日期','時間','Series','主題','id','留言',
                                                                        '留言好感度','留言Feature','URL','留言型號','非競品品牌',
                                                                        '非競品型號','文章好感度','文章feature'])

def GetTotalPage(url):

    total_page = 0
    
    All_Page_Content = GetPageContent(url)
    Pagination_Block = All_Page_Content.find('div',{'class':'l-navigation__item l-navigation__item--min'})
    if((Pagination_Block.text) == '\n'):
        total_page = 1
    else:
        Page_list = Pagination_Block.find_all('a',{'class':'c-pagination'})

        for i in range(len(Page_list)):
            temp = Parse(Page_list[i])

        total_page = int(temp)

    return total_page

def MoreThanOnePage(url):
    
    total_page = GetTotalPage(url)
    
    all_reviews = list()
    
    for i in range(1,total_page+1):
        new_url = url + '&p=' + str(i)
        page_reviews = GetPageReviews(new_url)
        all_reviews = all_reviews + page_reviews
        
    return all_reviews

def Read_URL():
    url_list = list()
    file_name = input('請輸入要讀取的txt檔(請加上副檔名)\n')
    file = open(file_name, 'r')
    for line in file:
        url = line.replace('\n', '').split(' ')
        url_list = url_list+url
    file.close()
    return url_list

def main():
    topic_list = list()
    all_reviews_list = list()
    
    topic_list = Read_URL()
    print('總共要爬 %d 篇文章' % len(topic_list))

    #print('===========================================\n')
    for i in range(len(topic_list)):
        temp = MoreThanOnePage(topic_list[i])
        all_reviews_list = all_reviews_list + temp
        
        sys.stdout.write("\r目前已處理 %d 篇" % (i+1))
        sys.stdout.flush()
    
    print('\n')
    #print('===========================================\n')  
    Save2Excel(all_reviews_list)

main()
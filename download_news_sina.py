import json
import csv
import threading
import multiprocessing
import json
from urllib.parse import urlencode
from urllib.request import urlopen,Request,urlparse,build_opener,install_opener
from urllib.error import URLError,HTTPError
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re






urls = []
num_thread = 40



with open("sina_url_uniq.csv") as fin:
    for line in fin:
        urls.append(line.strip())



def getnewsdetail(newsurl):                                        #获得单页的新闻内容
    result={}
    res=requests.get(newsurl)
    res.encoding='utf-8'
    soup=BeautifulSoup(res.text,'html.parser')
    result['title']=soup.select('.main-title')[0].text      #标题
    timesource=soup.select('.date-source span')[0].text  
    result['time']=datetime.strptime(timesource,'%Y年%m月%d日 %H:%M').strftime('%Y-%m-%d')              #时间
    result['place']=soup.select('.source')[0].text       #来源
    article=[]                                   #获取文章内容
    for p in soup.select('#article p')[:-1]:
        article.append(p.text.strip())
    articleall=' '.join(article)
    result['article']=articleall
    result['editor']=soup.select('#article p')[-1].text.strip('责任编辑：')     #获取作者姓名
#     result['comment_num']=getcommentcounts(newsurl)
    jresult = json.dumps(result)
    return jresult



def _thread(i):
    url_pos = i
    while url_pos <= len(url):
        try: 
            jresult = getnewsdetail(urls[url_pos])
            url_pos += num_thread
        except:
            url_pos += num_thread
            continue

        with open("sina_dump_" + str(i) ".jsonl", "a", encoding = utf-8) as fout:
            fout.write(jresult _ "\n")

        # only test
        break

def main():
    
    pool = multiprocessing.Pool()
    # 多进程  
    thread = threading.Thread(target=pool.map, args = (_thread, [x for x in range(0, 19)]))
    thread.start()
    thread.join()

if __name__ == "__main__":
    main()





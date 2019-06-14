

urls = []

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
    return result


def main():
    print(urls)

if __name__ == "__main__":
    main()
import csv
import threading
import multiprocessing
import json
from urllib.parse import urlencode
from urllib.request import urlopen,Request,urlparse,build_opener,install_opener
from urllib.error import URLError,HTTPError

def html_download(url):

    headers = {'User-Agent': "User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"}
    request = Request(url, headers=headers)
    try:
        html = urlopen(request).read().decode()
    except HTTPError as e:
        html = None
        print('[W] 下载出现服务器错误: %s' % e.reason)
        return None
    except URLError as e:
        html = None
        print("[E] 站点不可达: %s" % e.reason)
        return None
    return html

 
def api_info_manager(page):
    #http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&show_all=1&show_num=6000&tag=1&format=json
    comment_channel = [ 'gnxw', 'shxw','gjxw']
    for comment in comment_channel: 

        data= {
            'channel':'news',
            'cat_1':comment,
            'show_all':1,
            'show_num':6000,
            'tag':1,
            'page':page,
            'format':'json'
            }
        dataformat = 'http://api.roll.news.sina.com.cn/zt_list?'+urlencode(data)
        response = html_download(dataformat)
        #print(response)

        try:
            json_results = json.loads(response,encoding='utf-8')['result']['data']
        except:
            continue

        for info_dict in json_results:
            
            yield info_dict
 
 
fileheader = ['id','column','title','url','keywords','comment_channel','img','level','createtime','old_level','media_type','media_name']


# def write_csv_header(fileheader):
#     with open("新浪新闻.csv", "a", newline="") as csvfile:
#         writer = csv.DictWriter(csvfile, fileheader)
#         writer.writeheader()

    
def save_to_csv(result):
    with open("sina_url.csv", "a") as csvfile:
        print('正在写入csv文件中')
        csvfile.write(result["url"] + "\n")


def main(page):
    for res in api_info_manager(page):
        save_to_csv(res)



if __name__ == '__main__':
    #多线程  
    # write_csv_header(fileheader)
    pool = multiprocessing.Pool()
    # 多进程  
    thread = threading.Thread(target=pool.map,args = (main,[x for x in range(1, 200)]))
    thread.start()
    thread.join()
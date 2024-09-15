from tools import czbook,uukanshu#,twkan
#import tools.SixNineShuba as shuba69
import argparse
import os
import re
import time
import random
import requests
from bs4 import BeautifulSoup

def clean_filename(filename):
    # 移除非法字符
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def save_file(content,chapter,novel_name,chapter_name):
    if not os.path.isdir("./save"):
            os.mkdir("./save")
    if not os.path.isdir("./save/" + novel_name):
        os.mkdir("./save/" + novel_name)

    chapter_name = clean_filename(chapter_name)
    path = './save/'+novel_name+'/'+str(chapter)+'.'+chapter_name+'.txt'

    f = open(path,'w',encoding='UTF-8')
    f.write(content)
    f.close()

    #print(chapter_name," 儲存成功 !")

def bs4_init(url):
    url_content = requests.get(url)
    soup = BeautifulSoup(url_content.text,"html.parser")

    return soup

def get_chapter_url(novel_main_page_url,download_start_mode):
    soup = bs4_init(novel_main_page_url)

    if 'czbooks' in novel_main_page_url:
        novel_name = soup.find('span', class_='title')

        ul = soup.find('ul', class_='nav chapter-list')
        # find all li under ul and li class != volume
        all_li = [li for li in ul.find_all('li') if 'volume' not in li.get('class', [])]
        if len(all_li) >= download_start_mode:
            nth_li = all_li[download_start_mode-1]  # N-1 是因为列表索引从 0 开始
            content_url = nth_li.a['href']
        else:
            print("找不到第"+str(download_start_mode)+"話!")
            content_url = 'not_exist'
    elif 'uukanshu' in novel_main_page_url :
        novel_name = soup.find('h1', class_='booktitle')

        all_dd = soup.find_all('dd')
        if len(all_dd) >= download_start_mode:
            nth_dd = all_dd[download_start_mode-1]  # N-1 是因为列表索引从 0 开始
            content_url = nth_dd.a['href']
            content_url = '//uukanshu.cc'+content_url
        else:
            print("找不到第"+str(download_start_mode)+"話!")
            content_url = 'not_exist'

    return content_url,novel_name.text

if __name__ == '__main__':
    print("program start")
    parser = argparse.ArgumentParser(description="Novel Scraper")

    # parser_file_format = parser.add_mutually_exclusive_group(required=True)
    # parser_file_format.add_argument('-t',action='store_true',help='save to txt.')
    # parser_file_format.add_argument('-e',action='store_true',help='save to epub.')

    parser_download_interval = parser.add_mutually_exclusive_group(required=True)
    parser_download_interval.add_argument('-r',action='store_true',help='robot mode : download interval = 0s.')
    parser_download_interval.add_argument('-f',action='store_true',help='fast mode : download interval = 5~12s.')
    parser_download_interval.add_argument('-hm',action='store_true',help='human mode : download interval = 35~55s.')

    parser_download_start_point = parser.add_mutually_exclusive_group(required=True)
    parser_download_start_point.add_argument('-b',action='store_true',help='start at begin.')
    parser_download_start_point.add_argument('-c',type=int,dest='start_download_point',help='start at chapter XXX.')

    parser.add_argument('download_target',type=str,help='download target link.')

    args = parser.parse_args()

    if args.r:
        min_download_interval = max_download_interval = 0
    elif args.f:
        min_download_interval = 5
        max_download_interval = 12
    elif args.hm:
        min_download_interval = 35
        max_download_interval = 55

    if args.b:
        chapter = 1
    else:
        chapter = args.start_download_point

    novel_info = get_chapter_url(args.download_target,chapter)
    target_url = 'https:'+novel_info[0]
    novel_name = novel_info[1]

    while(target_url != None and target_url != 'https:not_exist'):       

        if 'czbooks.net' in target_url:
            feedback = czbook.get_content(target_url,min_download_interval,max_download_interval)
            target_url = feedback[0]
            save_file(feedback[1],chapter,novel_name,feedback[2])
        # elif 'twkan.com' in target_url:
        #     tw()
        elif 'uukanshu.cc' in target_url:
            feedback = uukanshu.get_content(target_url,min_download_interval,max_download_interval)
            target_url = feedback[0]
            save_file(feedback[1],chapter,novel_name,feedback[2])
        # elif '69shuba.pro' in target_url:
        #     s69()
        elif 'end_catch' in target_url:
            break
        else:
            print("不支援的網站!(",target_url,")")
            break

        chapter += 1
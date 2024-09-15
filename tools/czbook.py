from bs4 import BeautifulSoup
import requests
import time
import random

def wait(min,max,next_url):
    next_wait_time = random.randint(min,max)
    print(str(next_wait_time)+"秒後抓取下一話("+next_url+")!")
    time.sleep(next_wait_time)

def get_content(target_url,min_t,max_t):

    target = requests.get(target_url)
    soup = BeautifulSoup(target.text,"html.parser")

    get_content = soup.find('div', class_='content')
    content = get_content.text

    a_element = soup.find('a', class_='next-chapter')

    chapter_name = soup.find('div', class_='name')

    if a_element is None:
        print(chapter_name.text+"抓取完成!")
        print("結束抓取 !")
        return "not_exist",content,chapter_name.text
    else:
        print(chapter_name.text+"抓取完成!")
        next_url = "https:"+a_element["href"]
        wait(min_t,max_t,next_url)
        return next_url,content,chapter_name.text
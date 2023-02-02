import requests
from selenium import webdriver
import time
from lxml import etree
from fake_useragent import UserAgent
import os
from selenium.webdriver.chrome.options import Options
def music_parse():
    if not os.path.exists('./音乐'):
        os.mkdir("音乐")
    url=input('请输入歌曲地址')
    wb=webdriver.Chrome(executable_path="./chromedriver.exe",options=chrome_options)
    wb.get(url=url)
    data=wb.page_source
    wb.quit()
    tree=etree.HTML(data)
    music=tree.xpath('//*[@class="music"]/@src')[0]
    musicname="./音乐/"+tree.xpath('//*[@class="audioName"]/@title')[0]+".mp3"
    return music,musicname
def music_download(music,musicname):
    response=requests.get(url=music,headers=headers).content
    with open(musicname,"wb")as fp:
        fp.write(response)
        print("下载完成")
if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    headers={"User-Agent":UserAgent().random}
    music,musicname=music_parse()
    music_download(music,musicname)

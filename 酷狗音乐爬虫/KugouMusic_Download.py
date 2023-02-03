#!Python
# -*- encoding: utf-8 -*-
'''
1.文件名称 : MisicSpider.py
2.创建时间 : 2023/2/3
3.作者名称 : LRY
4.Python版本 : 3.10.x
'''

import os
import re
import getpass
import requests
from os import system


class Spider():
    def __init__(self):
        self.search_url = "http://songsearch.kugou.com/song_search_v2?callback=jQuery1124006980366032059648_1518578518932&keyword={}&page=1&pagesize=50&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1518578518934"
        self.url_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
        }
        self.geturl_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "cookie": "kg_mid=c597a55462cdb05b2f7dbcfe063c8e47; kg_dfid=1aF7SZ2FNXam3bTvyn0jEMtb; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1613640833; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1613641014",
            "if-modified-since": "Thu, 18 Feb 2021 11:14:12 GMT",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
        }
        self.api_url = "https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={}&album_id={}"

    def search(self):
        """用来为用户提供搜索的函数"""
        # 调用接口, 用来获取搜索的json数据
        search_url = self.search_url.format(input("请输入你要下载的音乐的名称:"))
        response = requests.get(search_url, headers=self.url_headers).text

        # 筛选出有用json数据
        pydata = eval(re.match(
            "jQuery1124006980366032059648_1518578518932((.*))", response).group(1))['data']['lists']
        number = len(pydata)
        number = range(0, number)
        for num in number:
            # 筛选并打印搜索结果
            song_name = pydata[num]['FileName'].replace(
                '<em>', '').replace('</em>', '').replace('<\/em>', '')
            song_num = str(num + 1)
            print(song_num + '.\t\t' + song_name)

        # 获取用户想要下载的歌曲
        num = int(input("请输入你要下载的音乐的序号:")) - 1
        song_name = pydata[num]['FileName'].replace(
            '<em>', '').replace('</em>', '').replace('<\/em>', '')
        # 根据用户输入， 获取重要的json数据，并调用下载函数
        song_hash = pydata[num]['FileHash']
        song_id = pydata[num]['AlbumID']
        self.download_music(song_name, song_hash, song_id)

    def download_music(self, name, hash, id):
        """通过api链接, 用来下载音乐的函数"""
        download_url = self.api_url.format(hash, id)
        response = requests.get(download_url, headers=self.geturl_headers)
        response.encoding = 'utf-8'
        music_data = eval(response.text.replace(
            'true', 'True').replace('false', 'False'))['data']
        # 用来获取数据中的音乐的下载链接
        music_url = music_data['play_url'].replace(
            '\\', '/').replace('//', '/')

        path = "C:\\Users\\%s\\Music\\" % (getpass.getuser())
        print("正在现在歌曲--> %s" % (name) + ' --> 请耐心等待...')
        print("下载链接为--> %s" % (music_url))

        music = requests.get(music_url, headers=self.url_headers).content

        with open(path + name + '.mp3', 'wb') as file:
            file.write(music)
        print("下载成功!!!（回车继续）")
        # 打卡下载目录
        start_directory = r"C:\\Users\\%s\\Music\\" % (getpass.getuser())
        os.startfile(start_directory)

        input()
        system('cls')



if __name__ == "__main__":
    # 运行程序
    spider = Spider()
    while True:
        spider.search()


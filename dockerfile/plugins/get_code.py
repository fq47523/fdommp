#!/usr/bin/env python3


import re
import time
import requests

class Getfile(object):  #下载文件

    def __init__(self,url):
        self.url=url

    def getheaders(self):
        try:
            r = requests.head(self.url)
            headers =  r.headers
            return headers
        except:
            print('无法获取下载文件大小')
            exit()

    def getfilename(self):  #获取默认下载文件名
        if 'Content-Disposition' in self.getheaders():
            print (self.getheaders())
            file = self.getheaders().get('Content-Disposition')
            print (file)
            filename = re.findall('filename=(.*)',file)
            print (filename)
            if filename:
                print (filename)
                return filename[0]

    def downfile(self,filename):  #下载文件
        self.r = requests.get(self.url,stream=True)
        with open(filename, "wb") as code:
            for chunk in self.r.iter_content(chunk_size=1024): #边下载边存硬盘
                if chunk:
                    code.write(chunk)
        time.sleep(1)



if __name__ == '__main__':

    url = 'https://codeload.github.com/fq47523/fdommp/zip/master'
    filename = Getfile(url).getfilename()
    Getfile(url).downfile(filename)

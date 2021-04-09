# -*- coding: utf-8 -*-
import codecs
import sys
import importlib
import requests
import tomd
import os

importlib.reload(sys)
 
global num_of_img 
global num_of_article 
global title 

num_of_img = 1
num_of_article = 18
title = 'article_'+str(num_of_article)
start_str = "<!--article detail-->\n"
end_str = "<!--/article detail-->\n"


currpath = os.getcwd()

save_file=currpath+r'\_post\markdown_'+str(num_of_article)+'.md'
save_text=currpath+r'\_post\website_'+str(num_of_article)+'.txt'
finalfile = currpath+r'\_post\2019-01-17-'+'article-'+str(num_of_article)+'.md'

def image_file(title):
    currpath = os.getcwd()
    if not os.path.exists(currpath+"/images/"+title):
        
        os.makedirs(currpath+r'/images/'+title)

def cut_text(text):
    temp = [];
    appending = False
    for line in text:
        if appending:
            temp.append(line)
        if line == start_str :
            appending = True
            index = text.index(line)
            temp.append(text[index-1])
        elif line == end_str : 
            appending = False
    temp.pop()
    return temp



def run():
    res = requests.get("http://www.openhw.org/newsinfo/449563.html")
    res.encoding = 'utf-8'
    f = codecs.open(save_text,'w+','utf-8')
    html = res.text
    #html = f.read()
    f.write(html)
    f.close()
    #print(html)
    image_file(title)
    mdTxt = tomd.Tomd(html,num_of_img,num_of_article,title).markdown
    #print('markdown :{}'.format(mdTxt))
    createFile(mdTxt)
 
 
def createFile(mdTxt):
    #print('系统默认编码：{}'.format(sys.getdefaultencoding()))
    #print('准备写入文件：{}'.format(save_file))
    #r+ 打开一个文件用于读写。文件指针将会放在文件的开头。
    #w+ 打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
    #a+ 打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
    f = codecs.open(save_file,'w+','utf-8')
    # f.write('###{}\n'.format(url))
    f.write(mdTxt)
    #f.write(mdTxt)
    f.close()
    #print('写入文件结束：{}'.format(f.name))
 
def finalize():
    f = codecs.open(save_file,'r+','utf-8')
    textfile = f.readlines()
    f.close()
    cutted_text = cut_text(textfile)
    f = codecs.open(finalfile,'w+','utf-8')
    f.writelines(cutted_text)
    f.close()   

run()
#above part has already got the page of the html
#below are to make the format to sit my target more
finalize()

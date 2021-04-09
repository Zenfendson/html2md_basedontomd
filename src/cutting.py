# -*- coding: utf-8 -*-
import codecs
import sys
import importlib
import requests
import re
import os

importlib.reload(sys)
 
currpath = os.getcwd()
 
num_of_article = 1
input_text=currpath+r'\_post\markdown'+str(num_of_article)+'.md'
save_editing=currpath+r'\_post\2019-01-17'+'article_'+str(num_of_article)+'.md'


start_str = "<!--article detail-->\n"
end_str = "<!--/article detail-->\n"
'''
def cutting(text):
    begin = re.search(start_str, text)
    end = re.search(end_str,text)
    if begin :
        f = codecs.open(save_editingfile,'w+','utf-8')
        newtext = re.findall(r'[.\n]',text,beign.end(),end.start())
        f.write(newtext)
        f.close()
'''

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

f = codecs.open(input_text,'r+','utf-8')
textfile = f.readlines()
f.close()
#print(textfile)
cutted_text = cut_text(textfile)
f = codecs.open(save_editing,'w+','utf-8')
f.writelines(cutted_text)
f.close()    
    

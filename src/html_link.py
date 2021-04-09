import re
import requests
import os

def download_image(content,i,title):
    #content = '<img alt="" height="692" src="//nwzimg.wezhan.hk/contents/sitefiles3601/18008104/images/3827319.png" width="703" />'
    pattern = r'<img.*?src="(.*?)".*?/>'
    save_image=currpath+r'/images/'+title+'/image_'+str(i)+'.png'
    judge = re.search(pattern,content)
    new=re.sub(pattern, r'![image_'+str(i)+']({{ site.baseurl }}/assets/images/'+'image_'+str(i)+'.png', content)
    print(judge)
    '''
    IMAGE_URL=re.sub(pattern, r'http:\g<1>', content)

    try:
        r = requests.get(IMAGE_URL,timeout=2)
        f = open(save_image,'wb')
        f.write(r.content) 
        f.close()
        i +=1
    except requests.exceptions.ConnectionError:
        print('image_unavailable') 
    '''
    return i

def image_file(title):
    currpath = os.getcwd()
    if not os.path.exists(currpath+"/images/"+title):
        
        os.makedirs(currpath+r'/images/'+title)

content = '<img alt="" height="692" src="//nwzimg.wezhan.hk/contents/sitefiles3601/18008104/images/3827319.png" width="703" />'
i = 1;
num_of_article = 1;
currpath = os.getcwd()
title = 'article_'+str(num_of_article)
image_file(title)
i = download_image(content,i,title)


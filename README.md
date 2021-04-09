# html2md_basedontomd

this is a personal tool which can help you tranform html source code into .md file based on tomd lib

# 输入 
1.url

2.number 表示第几个网页

# 输出 ：
### 一个website.txt 表示网页源代码
### 一个markdown file 为初步转换的文件，设计用于大部分网站
### 一个YYY-MMM-DDD-...md file，为满足个人博客的格式
### 一个/images/{target}/的文件夹，储存网站正文的图片

本段代码的主要增加的功能即为储存图片到本地

其中src/下implement.py 可输入URL转换， implement_local.py 转换本地txt格式的文件
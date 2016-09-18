#-*- coding:utf-8 -*-
__author__ = 'michaelxie'
# Editor Ying Liu ,for xml output
import urllib
import urllib2
import cookielib
import requests
import pyCookieCheat
from bs4 import BeautifulSoup
import cPickle
import re
import time
import xml.dom.minidom  
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getArticleList():
    contentList = open("wenzhang_full_backup.htm", "r").readlines()
    articleList = []
    # print len(contentList)
    #read article urls
    for content in contentList:
        s = 0
        while True:
            pos = content.find("/page/view?key", s)
            if pos == -1:
                break
            ending = content.find("\"", pos)
            articleList.append(content[pos : ending])
            s = ending
            # print "debug2"
    return articleList

def access1():
    #cookie file in Chrome
    filename = 'cookie.sqlite'
    cookie = cookielib.LWPCookieJar(filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    '''postdata = urllib.urlencode({
        'userName':'username,
        'password':'password'
    })
    loginUrl = 'https://passport.baidu.com/v2/?login&u=http%3A%2F%2Fwenzhang.baidu.com%2F'
    result = opener.open(loginUrl,postdata)'''
    #cookie.save(ignore_discard=True, ignore_expires=True)
    gradeUrl = 'http://wenzhang.baidu.com/'
    result = opener.open(gradeUrl)
    print result.read()

if __name__ == "__main__":
    output2txt = True
    #url="https://wenzhang.baidu.com/page/view?key=168a2f0785435838-1426607065"
    #writerList = open("output.txt", "w")

    f= open('output.xml', 'w')  
    #urls = ["https://wenzhang.baidu.com/page/view?key=168a2f0785435838-1426607065"]
    urls = getArticleList()
    # print urls
    articles = []
    #set xml root
    impl = xml.dom.minidom.getDOMImplementation()  
    dom = impl.createDocument(None, 'lofterBlogExport', None)  
    root = dom.documentElement
    description = dom.createElement('description') 
    BlogDomain = dom.createElement('BlogDomain') 
    ExportTime = dom.createElement('ExportTime') 
     
    root.appendChild(description)
    description.appendChild(BlogDomain)
    description.appendChild(ExportTime)
    nameT = dom.createTextNode("http://username.lofter.com")
    nameY = dom.createTextNode("2016-09-12 22:04")
    BlogDomain.appendChild(nameT)
    ExportTime.appendChild(nameY)

    for i, url in enumerate(urls):
        # Set up conn and cookies
        s = requests.Session()
        cookies = pyCookieCheat.chrome_cookies(url)
        # print cookies
        res = s.get("https://wenzhang.baidu.com"+url, cookies=cookies)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, 'html.parser')

        res2 = s.get(soup.body.iframe["src"], cookies = cookies)
        res2.encoding = "utf-8"
        soup2 = BeautifulSoup(res2.text, "html.parser")

        # Web scraping
        title = soup.title.string[1:-8]
        time_re = re.search(r'\d{4}-\d{2}-\d{2}', soup2.body.find('div', attrs={'class':'time-cang'}).string)
        time1 = time_re.group(0) if time_re else '0000-00-00'
        #process tags and encoding
        content = ""
        content_div = soup2.body.find('div', id='detailArticleContent_ptkaiapt4bxy_baiduscarticle')
        tags = content_div.find_all('p')
        if tags:
            # case 1: newer articles (>2011) use <p> or <p><span> to make new paragraphs
            for tag in tags:
                content = content + str(tag).replace('\n', '') + '\n'
        else:
            # case 2: older baidu articles use <br> to make new paragraphs
            for br in soup2.find_all('br'):
                br.replace_with('\n')
            content = content_div.text + '\n'

        content.replace("&nbsp;", " ")
        # Appending content images to the end
        # for img in content_div.find_all('img'):
        #     content += img['src'] + '\n'

        # Debugging
        #print i
        # print title
        # print time + '\n'
        # print content
        # print '+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n'

        articles.append((title, content, time1))

        # Write to text
        if output2txt:
            # writerList.write(title.encode("utf-8") + '\n')
            # writerList.write(time + '\n\n')
            # writerList.write(content.encode("utf-8") + '\n')
            # writerList.write('+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n')
            #set dom tree for xml output
            PostItem = dom.createElement('PostItem') 
            xmltitle = dom.createElement('title') 
            publishTime = dom.createElement('publishTime')  
            ttype = dom.createElement('type')  
            content1 = dom.createElement('content')  
            publishTime = dom.createElement('publishTime') 
            root.appendChild(PostItem)

            PostItem.appendChild(xmltitle)
            PostItem.appendChild(publishTime)
            PostItem.appendChild(ttype)
            PostItem.appendChild(content1)
            PostItem.appendChild(publishTime)

            timeArray = time.strptime(str(time1), "%Y-%m-%d")
            timeStamp = int(time.mktime(timeArray))

            item1 = dom.createCDATASection(title.encode("utf-8"))
            item2 = dom.createTextNode(str(int(timeStamp)*1000))
            item3 = dom.createTextNode("Text")
            item4 = dom.createCDATASection(content)
            xmltitle.appendChild(item1)
            publishTime.appendChild(item2)
            ttype.appendChild(item3)
            content1.appendChild(item4)
            #debug title
            print item1.nodeValue


    # Write to obj
    cPickle.dump(articles, open("articles.obj", "wb"))
    # f= open('output.xml', 'a')  
    #output xml to result file
    dom.writexml(f, addindent='  ', newl='\n')  
    f.close() 
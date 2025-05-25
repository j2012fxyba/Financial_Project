

import urllib.parse
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import threading





def spiderT(start_url):
    global page,count,DB,threads
    page=page+1
    print(page,start_url)
    try:
        res=urllib.request.Request(start_url,headers=head)
        respon=urllib.request.urlopen(res)
        html=respon.read().decode()
        soup=BeautifulSoup(html,'lxml')

            #图片标题
        a_list=soup.select("span[class='tw3_01_2_t'] a")
        for name in a_list:
            name.text
        print(name.text)

             #图片的发布时间
        b_list=soup.select("span[class='tw3_01_2_t'] b")
        for time in b_list:
            time.text
            print(time.text)
            
            #设置序号   %：格式化符号的开头   0：表示在数字前面填充0  6：表示整个数字的宽度为6  d：表示这是一个整数（decimal）。
        count+=1
        ID="%06d"%(count)   
        print(ID)     #然后将ID传递给download方法
            #获取href
        a_list=soup.select("span[class='tw3_01_2_t'] a")
        for href in a_list:
            link=href['href']
            #获取图片的跳转links  https://www.chinadaily.com.cn/a/202410/17/WS671058dca310f1265a1c8029.html
            new_link=urllib.parse.urljoin(start_url,href)     
            print(new_link)
           # tContent=downloadContent(new_link)   
                
            #拿到 img下面的src 地址 用于下载图片 src="//img2.chinadaily.com.cn/images/202410/17/671058dca310f1268d82f75f.jpeg"
            img_list=soup.select("span[class='tw3_01_2_p'] img")  

            for src in img_list:
                src=src.get('src')
                new_url=urllib.request.urljoin(start_url,src)
                point=new_url.rfind('.')
                if point>=0:
                    tExt=new_url[point+1:]  #将图片连接中 .后面的后缀保存在tExt 变量里
                t=threading.Thread(target=Download,args=[ID,new_url,tExt])
                t.start()
                threads.append(t)
                #调用数据库 
                DB.insert()
        #翻页 连接
        Next_page_Url=''
        fanye_links=soup.select("div[id='div_currpage'] a [class='pagestyle']")
        for link in fanye_links:
            if link.text=="Next":   #取出下一页的http请求地址
                href=link['href']
            if href.startswith('//www.'):  #先做出判断是否时 http连接的后缀部分
                Next_page_Url="https:"+href
                print(Next_page_Url)
            else:
                urllib.parse.urljoin(html,href)      #老版本的 python from urllib.parse import urljoin
                break    
            if Next_page_Url:
                #递归调用spider函数，传递 Next_page_url
                spiderT(Next_page_Url)    

    except Exception as e:
        print(e) 
    #new_url是下一页的下载图片地址
    def Download(ID,new_url,tExt):
        try:
            res=urllib.request.Request(new_url,headers=head)
            respon=urllib.request.urlopen(res)
            data=respon.read()
            imgName=ID+'.'+tExt
            with open("D:\\tool\\PythonTest\\pachong\\chinadaily\\download\\"+imgName,'ab') as file:
                file.write(data)
                print("download"+imgName)
        except Exception as e:
            print(e)


 
start_url="https://www.chinadaily.com.cn/travel/citytours/page_2.html"
head={'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'}
threads=[]



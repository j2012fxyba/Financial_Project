



import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import threading

#给定任意一个http请求地址并访问网站，返回一个html



def getHtml(start_url):
    #Request 创建一个请求对象函数 urlopen发送一个http请求连接,包含 请求头 请求方法体，可以在创建对象时船体更多参数
    #数据加密   用户认证
    res=urllib.request.Request(start_url,headers=head)
    respon=urllib.request.urlopen(res)
    data=respon.read()
    dammit=UnicodeDammit(data,['utf-8','gbk'])
    html=dammit.unicode_markup
    spiderImg(html)

def spiderImg(html):
    global threads

    try:
        urls=[]
        soup=BeautifulSoup(html,'lxml')
        html=soup.select("div[class='mb10 tw3_01_2']")
        img_list=soup.select("span[class='tw3_01_2_p'] img")  

        for src in img_list:
            #src['src']
            #拿到图片src地址
            src=src.get('src')
            #拼接start_url+src
            url=urllib.request.urljoin(start_url,src)
            print(url)


        #拿到图片下载内容
        a_list=soup.select("span[class='tw3_01_2_t'] a")
        for href in a_list:
            href=href['href']
            print(href)


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

        
        img_list=soup.select("span[class='tw3_01_2_p'] img")  

        for src in img_list:
            src=src.get('src')
            url=urllib.request.urljoin(start_url,src)
            
            if url not in urls:
                urls.append(url)
                t=threading.Thread(target=downImag,args=[url])
                
                #t.setDaemon(True)    3.3版本以后弃用
                #t.daemon(False)      #设置线程是 非守护  即后台执行
                t.daemon = False    #不能直接调用 是属性 不是方法
                t.start()
                threads.append(t)
                #downImag(url)     #切记 单线程的函数调用方法一定要注释掉 否则运行2次图片下载

    except Exception as er:
        print(er)  

        
    #根据拼接好的地址，下载图片
def downImag(url):      
    global count
    try:
        count=count+1
         #首先截取图片下载路径 中文件名
             #首先如果 url地址中倒数第5个是.说明是文件 .jepg
        if (url[len(url)-5]=='.'):

                  #将.前面5位取出 ，保存在ext中
            ext=url[len(url)-5:]
        else:
            ext=' '  #否则默认为空
        res=urllib.request.Request(url,headers=head)
        html=urllib.request.urlopen(res,timeout=100)
        data=html.read()

        fobj=open("D:\\tool\\PythonTest\\pachong\\chinadaily\\download\\"+str(count)+ext,'+ab') 
        fobj.write(data)
        fobj.close()
        print('download'+str(count)+ext)
            

    except Exception as erc:
        print (erc)

head={'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'}
start_url='https://www.chinadaily.com.cn/travel/citytours/page_2.html'
#urls=[
#   "https://www.chinadaily.com.cn/travel/citytours/page_2.html",
#    "https://www.chinadaily.com.cn/travel/citytours/page_3.html",
#    "https://www.chinadaily.com.cn/travel/citytours/page_5.html"]



count=0  
threads=[]     
getHtml(start_url)

for t in threads:
    t.join()
print('the end')



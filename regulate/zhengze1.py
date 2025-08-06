import re
import urllib.parse
import urllib.request



# 正则表达式截取 image标签
'''
html=
<div><img width="600" src="/static/download.png"></div>

print(html)'''


url='http://127.0.0.1:5000'
count=0
def download(src):
    global count
    try:
        
        respon=urllib.request.urlopen(src)
        data=respon.read()
        print()
        p=src.rfind('/')
        fileName=src[p+1:]   #截取img 连接中src中文件名后缀 .png 
        with open('downloadNew'+fileName,'wb') as file:
            file.write(data)  #将图片信息data写入本地down 文件里
            print('download sucess',fileName)

    except Exception as error: 
        print(error)

def getHtml():
        
        try:
            respon=urllib.request.urlopen(url)
            data=respon.read()
            html=data.decode()
            #从 <img 开始 中间匹配任意字符，以src=结尾
            print(html)
            reg=r'<img.+src='
            m=re.search(reg,html)  
            print(m)  #截取 src=前面的一段

            #选中代码，按下Tab 键 代码块会向右缩进,  Shift + Tab 键，代码块会向左取消缩进。
            while m:   #从src=后面开始找文件名

                a=m.end()  #从src后面的元素开始截取
                s=html[a:]
                #print(s)   # 截取的
                n=re.search(r"\".+\"",s)   #在s中找 ‘'\.+\'’ 2个斜杠中间的内容 即/static/
                b=n.end()   #从/static/后面开始找 ，即下载图片名称
                #print(b)
                src=s[1:b-1]
                print(src)
                src1=urllib.parse.urljoin(url,src)  #
                print(src1)
                download(src)
                html=s[n.end():]
                m=re.search(reg,html)
        except Exception as error:
            print(error)
getHtml()
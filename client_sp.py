

#做一个客户端，访问自己本地服务器的网址的信息


import urllib.request

def spider():

    url='http://127.0.0.1:5000/a'
    response=urllib.request.urlopen(url)
    data=response.read()
    html=data.decode()
    print(html)

spider()
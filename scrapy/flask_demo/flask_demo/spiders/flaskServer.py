import flask
import os



'''
flask 提供一个简单的文件服务器，返回服务器上读取文件给客户端。
用来处理客户端的请求，客户端请求一个特定文件getFile，服务器函数读取文件内容返回给客户端

'''
#__name__是Python中的一个特殊变量，它表示当前模块的名称
app=flask.Flask(__name__)



def getFile(fileName):
    #初始化了一个名为data的变量，用于存储文件的二进制内容
    data=b''
    if os.path.exists(fileName):
        obj=open(fileName,'rb')
        data=obj.read()
        obj.close()
    return data



#这是一个装饰器，它告诉Flask当用户访问网站根目录/in,时应该调用哪个函数
@app.route('/ind')
def index():
    #这行代码调用了getFile函数，并返回了books.html文件的内容.也就是说给参数fileName 指定了book.html的内容
    return getFile('D:\\tool\\scrapydemo\\flaskDemo\\flaskDemo\\spiders\\books.html')


#在 Flask 中，尖括号 <> 用于定义路由中的动态部分.
# 当你使用 @app.route('/<section>') 时，你是在告诉 Flask，任何匹配 / 后跟任何字符串的 URL 都应该由 process 函数来处理。
# 这个字符串将被赋值给 section 参数
#例如，如果用户访问 /home，section 参数将被设置为 'home'。
#如果用户访问 /about，section 参数将被设置为 'about'。这样，你可以根据 section 的值来决定返回哪个文件的内容

@app.route('/<section>')
def process(section):
    data=''
    if section !='':  #如果section参数不为空，调用getFile函数，并返回section文件内容
        data=getFile(section)    ##此时fileName参数被设置为section
    return data


#定义main函数
if __name__=='__main__':
    app.run()


#selenium.xpath()的语法：



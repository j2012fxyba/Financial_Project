import flask



#编写一个爬虫程序，获取a.html网页的内容 保存在file,然后read 返回打印出来
app=flask.Flask(__name__)


@app.route('/a')
def index():
   file=open('D:\\tool\\PythonTest\\flask\\flaskDemo\\a.html','rb')
   data=file.read()
   html=data.decode()
  
   return html

if __name__=="__main__":
    app.debug=True
    app.run()

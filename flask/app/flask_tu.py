from flask import Flask, send_from_directory
from flask import Flask,send_file
import os
import flask

app = Flask(__name__)

# 方法1：使用默认静态文件夹,<path:filename> 是动态路径转换器，可以匹配包含斜线的文件名
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, 'test3.jpg')



#通过flask 打开本地图片img ,客户端通过浏览器访问地址时，返回图片信息
#现在出现一个问题，浏览器访问页面后，图片后缀没有了，导致下载下来的图片，需要手动添加图片后缀
@app.route('/img')
def get_img():
    img_path='D:\\tool\\PythonTest\\flask\\flask_templates\\static\\test3.jpg'

    #默认是二进制方式打开,服务器获取的就是二进制，
    data=open(img_path,'rb')
    img=data.read()
    data.close()
    
   
    response=flask.make_response(img)
     # 得告知浏览器此文件类型为图片，希望用图片的方式将二进制字节码转换为图片格式,避免下载下来是乱码，打不开
    response.headers['content-type']='image/jpeg'
    return response

if __name__=='__main__':
    app.debug=True
    app.run()


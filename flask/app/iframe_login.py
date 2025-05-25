

import flask
import os

app=flask.Flask('web',static_folder='D:\\tool\\PythonTest\\flask\\flask_templates\\static',
                template_folder='D:\\tool\\PythonTest\\flask\\flask_templates\\templates'
                )



#获取客户端输入的user  pwd
@app.route('/',methods=['GET','POST'])
def index():
    #登录初始化session，服务器端给session 默认初始化login的缓存，默认为空（如Redis）
    flask.session['login']=''   
    #session的值必须是可以json序列话的 （字符串、数字、列表、字典等）
    user=flask.request.values.get('user','')
    pwd=flask.request.values.get('pwd','')

    if user=='admin' and pwd=='123':
        flask.session['login']='ok'   #如果用户名和密码 输入正确，则给session 赋值login=ok
        return flask.redirect('/show') #重定向到 show页面
    else:
        return flask.render_template('iframe_index.html')

#许多web框架 如flask Django FastAPI等 强制要求路由url要以 /开头
# 路由器的 URL 路径通常以 / 开头，表示它是从根路径开始的绝对路径


@app.route('/show')   
def show():
    if flask.session.get('login')!='ok':  #检查session中的 login 如果为空或者不为 OK 就重定向到index初始界面
        return flask.redirect('/')     #如果条件成立则返回 book.html
    else:
        return flask.render_template('books.html')



app.secret_key=os.urandom(16)  #随机字符串 16位
app.debug=True
app.run()
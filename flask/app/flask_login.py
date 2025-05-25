import flask
from flask import Flask,request,redirect,render_template,session


app=flask.Flask('web',static_folder='D:\\tool\\PythonTest\\flask\\flask_templates\\static',
                template_folder='D:\\tool\\PythonTest\\flask\\flask_templates\\templates'
                )


''''
flask 动态获取页面ajax 元素 包含 summit and input canle  and requeset  
'''

#任务：1 html 页面做一个 用户登录login.html， input password and user 登录成功返回手机信息，
    #登录失败，提示输入有误 



@app.route('/login',methods=['GET','POST'])
def login():
    #flask 获取用户输入的user  password 
    #这是一个 3目运算，如果有值就将值 赋值给 user  如果值为空就 返回''
    

    if request.method=='POST':
        user=request.form.get('user','').strip()

        pwd=request.form.get('pwd','').strip()

        if user =='admin' and pwd=='123':
        #redirect 请求重定向
            return redirect('/show')
    else:
        return render_template('login.html')
    
@app.route('/show',methods=['GET','POST'])   
def show():
    return flask.render_template('show.html')


app.debug=True
app.run()


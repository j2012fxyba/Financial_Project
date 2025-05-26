import flask
from flask import Flask,request,redirect,render_template,session


app=flask.Flask('web',static_folder='D:\\tool\\PythonTest\\flask\\flask_templates\\static',
                template_folder='D:\\tool\\PythonTest\\flask\\flask_templates\\templates'
                )



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


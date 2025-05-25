import flask



app=flask.Flask(__name__,static_folder='D:\\tool\\PythonTest\\flask\\flask_templates\\images',
                template_folder='D:\\tool\\PythonTest\\flask\\flask_templates\\templates')


#从 home 本地根目录访问 books.html 然后跳转至 program.html   database.html   network.html各级子目录

@app.route('/home')
def index():
    #通过 Flask 路由动态跳转（推荐）
    #如果文件在 templates/ 中，需通过 render_template 渲染。
    return flask.render_template('books.html')



#开启路由器渲染
@app.route('/books.html') 
def books():
    return flask.render_template('books.html')

@app.route('/database.html') 
def database():
    return flask.render_template('database.html')


@app.route('/program.html')
def program():
    return flask.render_template('program.html')

@app.route('/network.html')
def network():
    return flask.render_template('network.html')

@app.route('/python.html')
def python():
    return flask.render_template('python.html')

@app.route('/java.html')
def java():
    return flask.render_template('java.html')

@app.route('/mysql.html')
def mysql():
    return flask.render_template('mysql.html')

if __name__=='__main__':
    app.debug=True
    app.run()
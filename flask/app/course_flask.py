
import flask
import json


app=flask.Flask('web',static_folder='D:\\tool\\PythonTest\\flask\\flask_templates\\images',
                template_folder='D:\\tool\\PythonTest\\flask\\flask_templates\\templates'
                )



@app.route('/get_course',methods=['GET','POST'])
def get_course():
    return flask.render_template('course.html')


@app.route('/show_course')
def show_course():
    reslu=[]
    books={'python':['python程序设计','python网络爬虫','python数据分析'],
           'java':['java程序设计','java高级语言','java实践项目'],
           'c':['c语言基础','C 语言工业化应用','C语言高级应用']
    }
    
    course=flask.request.values.get('course','')
    if course in ['python','java','c']:
        reslu=books[course]
    return json.dumps(reslu)


app.debug=True
app.run()
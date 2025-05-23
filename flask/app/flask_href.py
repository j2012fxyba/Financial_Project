import flask

app=flask.Flask(__name__)

#中文
@app.route('/chin')
def chinese():
    html= "<h1>大家好<h1>"
    html+="<a href='/eng'>english</a>"
    return html


#英文
@app.route('/eng')
def english():
    html="<h1>hello </h1>"
    html+='<a href="/chin">中文</a>'
    return html

if __name__=='__main__':
    app.debug=True
    app.run()

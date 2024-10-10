from flask import Flask , render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        # print('POST')
        title = request.form['title']
        desc = request.form['desc']
    todo = ToDo(title=title,desc=desc)
    db.session.add(todo)
    db.session.commit()
    allTodo = ToDo.query.all()
    # print(allTodo)
    # return 'Hello, World!'
    return render_template('index.html',allTodo=allTodo)

@app.route('/show')
def products():
    allTodo = ToDo.query.all()
    print(allTodo)
    return 'Products'

class ToDo(db.Model):
    SNo = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(1000),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.title} - {self.desc}"


if __name__=='__main__':
    app.run(debug=True,port=8001)
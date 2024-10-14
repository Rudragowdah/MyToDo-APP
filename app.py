from flask import Flask , render_template, request, redirect
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
        print(title)
        desc = request.form['desc']
        todo = ToDo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = ToDo.query.all()
    # print(allTodo)
    # return 'Hello, World!'
    return render_template('index.html',allTodo=allTodo)

@app.route('/delete/<int:SNo>')
def delete(SNo):
    todo = ToDo.query.filter_by(SNo=SNo).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:SNo>',methods=['GET','POST'])
def update(SNo):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo.query.filter_by(SNo=SNo).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = ToDo.query.filter_by(SNo=SNo).first()
    return render_template('update.html',todo=todo)



class ToDo(db.Model):
    SNo = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(1000),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.title} - {self.desc}"


if __name__=='__main__':
    app.run(debug=True,port=8001)
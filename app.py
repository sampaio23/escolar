from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schools.db'
db = SQLAlchemy(app)

class School(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    neigh = db.Column(db.String(200), nullable = False)
    students = db.Column(db.Integer, default = 0)
    endow = db.Column(db.Float)

    def __repr__(self):
        return '<Task %r>' % self.id

class Classes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    students = db.Column(db.Integer, default = 0)
    school = db.Column(db.String(200), nullable = False)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['nome']
        bairro = request.form['bairro']
        verba = request.form['verba']

        new_school = School(name = name, neigh = bairro, endow = verba)

        try:
            db.session.add(new_school)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue"

    else:
        schools = School.query.order_by(School.id).all()
        return render_template('index.html', schools = schools)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue'

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue'
    else:
        return render_template('update.html',task = task)


if __name__ == "__main__":
    app.run(debug = True)

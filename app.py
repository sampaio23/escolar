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

@app.route('/excluir_escola/<int:id>')
def delete_school(id):
    school_to_delete = School.query.get_or_404(id)

    try:
        db.session.delete(school_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue'

@app.route('/excluir_turma', methods=['GET'])
def delete_class():
    data = request.args.to_dict()
    sc = data['sc']
    id = data['cl']
    class_to_delete = Classes.query.get_or_404(id)
    school_sel = School.query.filter_by(id = sc).all()
    school_name = school_sel[0].name
    classes = Classes.query.filter_by(school = school_sel[0].name).all()

    alunos = class_to_delete.students
    total_alunos = school_sel[0].students
    total_alunos = total_alunos - int(alunos)

    school = School.query.get_or_404(sc)
    school.students = total_alunos


    try:
        db.session.delete(class_to_delete)
        db.session.commit()
        return redirect('/turmas/'+str(sc))
    except:
        return 'There was an issue'

@app.route('/turmas/<int:id>', methods=['POST', 'GET'])
def update(id):
    school_sel = School.query.filter_by(id = id).all()
    school_name = school_sel[0].name
    classes = Classes.query.filter_by(school = school_sel[0].name).all()

    if request.method == 'POST':
        turma = request.form['turma']
        alunos = request.form['alunos']
        total_alunos = school_sel[0].students
        total_alunos = total_alunos + int(alunos)

        new_class = Classes(name = turma, students = alunos, school = school_sel[0].name)
        school = School.query.get_or_404(id)
        school.students = total_alunos

        try:
            db.session.add(new_class)
            db.session.commit()

        except:
            return "There was an issue"
        
        return redirect('/turmas/'+str(id))

    else:
        return render_template('turmas.html', classes = classes, school_name = school_name, id = id)


if __name__ == "__main__":
    app.run(debug = True)

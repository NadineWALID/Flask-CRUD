from flask_sqlalchemy import SQLAlchemy
from datetime import date
from manage import app


db = SQLAlchemy(app)





class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    title_id = db.Column(db.Integer,db.ForeignKey('title.id', ondelete='CASCADE'))
    date_of_hiring=db.Column(db.Integer)
    salary=db.Column(db.Integer)
    department_id=db.Column(db.Integer,db.ForeignKey('department.id', ondelete='CASCADE'))

    def __init__(self, name,title_id,date_of_hiring, department_id):
        self.name=name
        self.title_id=title_id
        self.date_of_hiring=date_of_hiring
        current_year = date.today().year
        years_of_exp=int(current_year)-int(date_of_hiring)
        title=Title.query.filter_by(id=title_id).first()
        self.salary= title.starting_salary  + years_of_exp*100
        self.department_id=department_id

    def __repr__(self):
        return '<User %r> %self.username'

class Department(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    department_name = db.Column(db.String(80),unique=True)
    

    def __init__(self, department_name):
        self.department_name=department_name
        

    def __repr__(self):
        return '<User %r> %self.username'


class Title(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title_name = db.Column(db.String(80),unique=True)
    starting_salary = db.Column(db.Integer)

    def __init__(self, title_name,starting_salary):
        self.title_name=title_name
        self.starting_salary=starting_salary

        

    def __repr__(self):
        return '<User %r> %self.username'
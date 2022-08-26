from flask import Flask, redirect, url_for, render_template
from flask import request
from datetime import date
from sqlalchemy.exc import IntegrityError
from models import db
from models import User
from models import Department
from models import Title
from manage import app





@app.route("/")
def home():
    users=db.session.query(
        User.id,
        User.name,
        User.date_of_hiring,
        User.salary,
        Title.title_name,
        
    ).join(
        Title,
        User.title_id == Title.id,
        isouter=True,
    ).all()
    departments = Department.query.all()
    current_year = date.today().year
    return render_template("index.html", users=users, departments=departments, current_year=current_year)

@app.route("/addemployee")
def add_user():
    titles = Title.query.all()
    departments = Department.query.all()
    current_year = date.today().year
    return render_template("create_user.html",departments=departments,current_year=current_year,titles=titles)

@app.route("/adddepartment")
def add_department():
    return render_template("create_department.html",department=None)

@app.route("/showemployees")
def show_employees():
    name=request.args.get('department')
    if name != '0' :
        users = db.session.query(
        User.id,
        User.name,
        User.date_of_hiring,
        User.salary,
        User.department_id,
        Title.title_name,
        ).filter_by(department_id=name).join(
        Title,
        User.title_id == Title.id,
        isouter=True,
        )
    else:
        users = db.session.query(
        User.id,
        User.name,
        User.date_of_hiring,
        User.salary,
        User.department_id,
        Title.title_name,
        ).join(
        Title,
        User.title_id == Title.id,
        isouter=True,
        )

    
    departments = Department.query.all()
    current_year = date.today().year
    return render_template("index.html", users=users, departments=departments, current_year=current_year)

@app.route("/postuser",methods=['POST'])
def post_user():
    user = User(request.form['name'],request.form['title'],request.form['date'],request.form['department'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/posttitle",methods=['POST'])
def post_title():
    title= Title(request.form['title'],request.form['salary'])
    db.session.add(title)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    return redirect(url_for("add_user"))

@app.route("/postdepartment",methods=['POST'])
def post_department():
    dep = Department(request.form['name'])
    db.session.add(dep)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    return redirect(url_for("show_departments"))

@app.route("/updateuser<user_id>")
def update_user(user_id):
    user=User.query.get(user_id)
    titles = Title.query.all()
    departments = Department.query.all()
    current_year = date.today().year
    return render_template("update_user.html",user=user,departments=departments, current_year=current_year, titles = titles)

@app.route("/updatedepartment<department_id>")
def update_department(department_id):
    department=Department.query.get(department_id)
    return render_template("create_department.html",department=department)

@app.route("/deleteuser<user_id>")
def delete_user(user_id):
    user=User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/deletedepartment<department_id>")
def delete_department(department_id):
    department=Department.query.get(department_id)
    db.session.delete(department)
    db.session.commit()
    return redirect(url_for("show_departments"))

@app.route("/deletetitle<title_id>")
def delete_title(title_id):
    title=Title.query.get(title_id)
    db.session.delete(title)
    db.session.commit()
    return redirect(url_for("add_user"))

@app.route("/postupdateduser",methods=['POST'])
def post_update_user():
    user=User.query.get(request.form['user_id'])
    user.name = request.form['name']
    user.title_id= request.form['title']
    user.date_of_hiring = request.form['date']
    user.salary = request.form['salary']
    user.department_id = request.form['department']
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/postupdateddepartment",methods=['POST'])
def post_update_department():
    department=Department.query.get(request.form['dep_id'])
    department.department_name = request.form['name']
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    return redirect(url_for("show_departments"))

@app.route("/showdepartments")
def show_departments():
    departments = Department.query.all()
    return render_template("all_departments.html", departments=departments)

if __name__=="__main__":
    app.run()

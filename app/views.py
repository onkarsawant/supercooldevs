from app import app
import os
from flask import Flask, request, jsonify , render_template
from flask_sqlalchemy import SQLAlchemy


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://startyounguk:\'DBpassword@01\'@localhost/startyounguk'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'hi'
db = SQLAlchemy(app)



@app.route("/")
def hello():
    return render_template("index.html")

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(80), unique=True, nullable=False)
    student_age = db.Column(db.Integer , nullable=False)

    def __init__(self, student_name,student_age):
        self.student_name = student_name
        self.student_age = student_age 

@app.route("/add", methods=['POST'])
def add_student():
    name=request.args.get('name')
    age=request.args.get('age')
    location=request.args.get('location')
    sex=request.args.get('sex')
    contact=request.args.get('contact')
    area_of_interest=request.args.get('area_of_interest')
    school=request.args.get('school')
    try:
        student=Student(
            name=name,
            age=age,
            location=location,
            sex=sex,
            contact=contact,
            area_of_interest=area_of_interest,
            school=school
        )
        db.session.add(student)
        db.session.commit()
        return "Student added. student id={}".format(student.id)
    except Exception as e:
	    return(str(e))



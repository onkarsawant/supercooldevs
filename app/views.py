import os
from sys import set_coroutine_origin_tracking_depth
from flask import Flask, request, jsonify , render_template
from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://startyounguk:DBpassword01@startyoungukdb.postgres.database.azure.com/startyoungukdb'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class School(db.Model):
  __tablename__='school'
  sc_id=db.Column(db.Integer,primary_key=True)
  sc_name=db.Column(db.String(20))
  sc_contact=db.Column(db.String(15))
  sc_email=db.Column(db.String(40))
  sc_address=db.Column(db.String(40))

  def __init__(self,sc_id,sc_name,sc_contact,sc_email,sc_address):
    self.sc_id=sc_id
    self.sc_name=sc_name
    self.sc_contact=sc_contact
    self.sc_email=sc_email
    self.sc_address=sc_address


class Student(db.Model):
  __tablename__='students'
  id=db.Column(db.Integer,primary_key=True)
  fname=db.Column(db.String(20))
  lname=db.Column(db.String(20))
  st_age=db.Column(db.Integer)
  st_location=db.Column(db.String(40))
  st_contact=db.Column(db.String(40))
  st_school=db.Column(db.String(40))


  def __init__(self,fname,lname,st_age,st_location,st_contact,st_school):
    self.fname=fname
    self.lname=lname
    self.st_age=st_age
    self.st_location=st_location
    self.st_contact=st_contact
    self.st_school=st_school


@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/add")
def addStudent():
    return render_template("addStudent.html")


@app.route("/addSchool")
def addSchool():
    return render_template("addSchool.html")



@app.route("/submit", methods=['POST'])
def submit():
  fname= request.form['fname']
  lname=request.form['lname']
  st_age=request.form['st_age']
  st_location=request.form['st_location']
  st_contact=request.form['st_contact']
  st_school=request.form['st_school']

  student=Student(fname,lname,st_age,st_location,st_contact,st_school)
  db.session.add(student)
  db.session.commit()

  #fetch a certain student2
  studentResult=db.session.query(Student).filter(Student.id==1)
  for result in studentResult:
    print(result.fname)

  return render_template('success.html', data=fname)



@app.route("/submitSchool", methods=['POST'])
def submitSchool():
  sc_id= request.form['sc_id']
  sc_name=request.form['sc_name']
  sc_contact=request.form['sc_contact']
  sc_email=request.form['sc_email']
  sc_address=request.form['sc_address']

  school=School(sc_id,sc_name,sc_contact,sc_email,sc_address)
  db.session.add(school)
  db.session.commit()

  #fetch a certain student2
  schoolResult=db.session.query(School).filter(School.sc_id==1)
  for result in schoolResult:
    print(result.sc_name)

  return render_template('success.html', data=sc_name)
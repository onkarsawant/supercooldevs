import os
from os import environ as env
from sys import set_coroutine_origin_tracking_depth
from flask import Flask, request, jsonify , render_template
from flask_sqlalchemy import SQLAlchemy
from app import app

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://startyounguk:DBpassword01@startyoungukdb.postgres.database.azure.com/postgres'
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = env["SQLALCHEMY_DATABASE_URI"]
# String (Mapped Name)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = env["SQLALCHEMY_TRACK_MODIFICATIONS"]


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
  st_hby=db.Column(db.String(10))
  st_school=db.Column(db.String(40))


  def __init__(self,fname,lname,st_age,st_location,st_contact,st_hby,st_school):
    self.fname=fname
    self.lname=lname
    self.st_age=st_age
    self.st_location=st_location
    self.st_contact=st_contact
    self.st_hby=st_hby
    self.st_school=st_school

class Sponsor(db.Model):
  __tablename__='sponsor'
  id=db.Column(db.Integer,primary_key=True)
  fname=db.Column(db.String(20))
  lname=db.Column(db.String(20))
  sp_age=db.Column(db.Integer)
  sp_location=db.Column(db.String(40))
  sp_contact=db.Column(db.String(40))
  sp_email=db.Column(db.String(40))
  sp_hby=db.Column(db.String(10))
  sp_occ=db.Column(db.String(40))


  def __init__(self,fname,lname,sp_age,sp_location,sp_contact,sp_email,sp_hby,sp_occ):
    self.fname=fname
    self.lname=lname
    self.sp_age=sp_age
    self.sp_location=sp_location
    self.sp_contact=sp_contact
    self.sp_hby=sp_hby
    self.sp_occ=sp_occ
    self.sp_email=sp_email


@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/addStudent")
def addStudent():
    return render_template("addStudent.html")

@app.route("/addSponsor")
def addSponsor():
    return render_template("addSponsor.html")

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
  st_hby=request.form['hobby']
  st_school=request.form['st_school']

  student=Student(fname,lname,st_age,st_location,st_contact,st_hby,st_school)
  db.session.add(student)
  db.session.commit()

  #fetch a certain student2
  studentResult=db.session.query(Student).filter(Student.id==1)
  for result in studentResult:
    print(result.fname)

  return render_template('success.html', data=fname)



@app.route("/submitSponsor", methods=['POST'])
def submitSponsor():
  fname= request.form['fname']
  lname=request.form['lname']
  sp_age=request.form['sp_age']
  sp_location=request.form['sp_location']
  sp_contact=request.form['sp_contact']
  sp_email=request.form['sp_email']
  sp_hby=request.form['hobby']
  sp_occ=request.form['sp_occ']

  sponsor=Sponsor(fname,lname,sp_age,sp_location,sp_contact,sp_email,sp_hby,sp_occ)
  db.session.add(sponsor)
  db.session.commit()

  #fetch a certain student2
  sponsorResult=db.session.query(Sponsor).filter(Sponsor.id==1)
  for result in sponsorResult:
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
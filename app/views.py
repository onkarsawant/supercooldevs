import os
import json
from os import environ as env
from sys import set_coroutine_origin_tracking_depth
from flask import Flask, request, jsonify , render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select , and_
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
  st_spon_status=db.Column(db.String(5))
  st_is_appr=db.Column(db.String(5))


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
  sp_is_appr=db.Column(db.String(5))


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

@app.route("/home")
def home():
    return render_template("index2.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/loginok")
def loginok():
    return render_template("loginok.html")

@app.route("/addStudent")
def addStudent():
    return render_template("addStudent2.html")

@app.route("/addSponsor")
def addSponsor():
    return render_template("addSponsor.html")

@app.route("/addSchool")
def addSchool():
    return render_template("addSchool2.html")

@app.route("/successStories")
def successStories():
    return render_template("blog.html")


@app.route("/fetchDB")
def fetchDBPulic():
    sc_all = School.query.all()
    st_all = Student.query.all()
    sp_all = Sponsor.query.all()

    st_results = [
            {
                'name': student.fname,
                'lastname': student.lname,
                'st_school': student.st_school,
                'st_spon_status': student.st_spon_status,
            } for student in st_all ]
    sc_results = [
            {
                'sc_id': school.sc_id,
                'sc_name': school.sc_name
            } for school in sc_all ]
    sp_results = [
            {
                'name': sponsor.fname,
                'lastname': sponsor.lname,
                'sp_age': sponsor.sp_age,
                'sp_location': sponsor.sp_location
            } for sponsor in sp_all ]
    

    st_pending_scrng_stmt = select([Student.fname,Student.lname]).where(and_( Student.st_is_appr==None)) 
    st_pending_scrng = [dict(row) for row in db.session.execute(st_pending_scrng_stmt)]

    st_pending_spnsr_stmt = select([Student.fname,Student.lname]).where(and_( Student.st_is_appr=='yes', Student.st_spon_status==None)) 
    st_pending_spnsr = [dict(row) for row in db.session.execute(st_pending_spnsr_stmt)]

    return { "School's registered": len(sc_results) , "Total Students": len(st_results) , "Students pending sponsorship": len(st_pending_spnsr) , "Students under screening and onboarding": len(st_pending_scrng), "Our Sponsors": len(sp_results) }



@app.route("/fetchDBPriv")
def fetchDBPrivate():
    sc_all = School.query.all()
    st_all = Student.query.all()
    sp_all = Sponsor.query.all()

    st_results = [
            {
                'name': student.fname,
                'lastname': student.lname,
                'st_school': student.st_school,
                'st_spon_status': student.st_spon_status,
                'st_age': student.st_age,
                'st_location': student.st_location,
                'st_contact': student.st_contact,
                'st_hby': student.st_hby,
                'st_is_appr': student.st_is_appr
            } for student in st_all ]
    sc_results = [
            {
                'sc_id': school.sc_id,
                'sc_name': school.sc_name,
                'sc_contact': school.sc_contact,
                'sc_email': school.sc_email,
                'sc_address': school.sc_address
            } for school in sc_all ]
    sp_results = [
            {
                'name': sponsor.fname,
                'lastname': sponsor.lname,
                'sp_age': sponsor.sp_age,
                'sp_location': sponsor.sp_location,
                'sp_contact': sponsor.sp_contact,
                'sp_hby': sponsor.sp_hby,
                'sp_occ': sponsor.sp_occ,
                'sp_email': sponsor.sp_email,
                'sp_is_appr': sponsor.sp_is_appr
            } for sponsor in sp_all ]
    

    sp_pending_scrng_stmt = select([ Sponsor.fname , Sponsor.lname , Sponsor.sp_age , Sponsor.sp_location,Sponsor.sp_contact , Sponsor.sp_hby , Sponsor.sp_occ , Sponsor.sp_email]).where(and_( Sponsor.sp_is_appr==None)) 
    sp_pending_scrng = [dict(row) for row in db.session.execute(sp_pending_scrng_stmt)]

    st_pending_scrng_stmt = select([Student.fname,Student.lname,Student.st_school,Student.st_age,Student.st_location,Student.st_contact,Student.st_hby]).where(and_( Student.st_is_appr==None)) 
    st_pending_scrng = [dict(row) for row in db.session.execute(st_pending_scrng_stmt)]

    st_pending_spnsr_stmt = select([Student.fname,Student.lname]).where(and_( Student.st_is_appr=='yes', Student.st_spon_status==None)) 
    st_pending_spnsr = [dict(row) for row in db.session.execute(st_pending_spnsr_stmt)]


    return (render_template('adminDashboard.html', Stdata=st_results , Scdata=sc_results , StPnSp=st_pending_scrng , SpPnSp=sp_pending_scrng))



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

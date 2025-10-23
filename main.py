#Flask module for using flask
#Sqlalchemy library for connecting frontend and backend(mysql) using python
#importing flask
from flask import Flask,render_template,request,session,redirect,url_for,flash

#importing sqlalchemy
from flask_sqlalchemy import SQLAlchemy


#importing flask login for encrypted & decrypted password stored in db
from flask_login import UserMixin

#for hashed function which helps in encryption & decryption
from werkzeug.security import generate_password_hash,check_password_hash

from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user

#to send email
from flask_mail import Mail

#For importing json file
import json




local_server = True
app = Flask(__name__)
app.secret_key = 'adityasinha'          #secret_key


#This is for unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'




@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


#app.config['SQLALCHEMY_DATABASE_URL'] = 'mysql://username:password@localhost/database_table_name'               #for loading bms(bus management system) in main.py file
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/student'                                            #for xampp by default we have username as root and password as nothing and database name is bms for me  
db=SQLAlchemy(app)          #passing app config to database



class Admin(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(50))
    Email = db.Column(db.String(100),unique=True)
    Password = db.Column(db.String(1500))


class Studentdetails(db.Model):
    SerialNo=db.Column(db.Integer,primary_key=True)
    RegNo=db.Column(db.Integer,unique=True)
    Firstname=db.Column(db.String(50))
    Lastname=db.Column(db.String(50))
    Grade=db.Column(db.Integer)
    ParentName=db.Column(db.String(100))
    ContactDetails=db.Column(db.String(12))
    DateofAdmission=db.Column(db.String(50),nullable=False)
    AmountPaid=db.Column(db.Integer)
    # PaymentInfo=db.Column(db.String(100),nullable=False)
    BatchNo=db.Column(db.String(5),nullable=False)
    BatchStartDate=db.Column(db.String(50),nullable=False)
    BatchTiming=db.Column(db.String(20))




@app.route('/')                     #for routing.....get an IP address
def index():
    return render_template('index.html')



#For inserting values taken from ticket page  i.e ticket.html

@app.route('/student',methods=['POST','GET'])
@login_required
def student ():    

    if request.method=="POST":
        regno=request.form.get('regno')
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        grade=request.form.get('grade')
        parentname=request.form.get('parentname')
        contact=request.form.get('contact')
        doa=request.form.get('doa')
        amount=request.form.get('amount')
        # payment=request.form.get('paymentinfo')
        batchno=request.form.get('batchno')
        batchdate=request.form.get('batchdate')
        batchtime=request.form.get('batchtime')

        
        user1=Studentdetails.query.filter_by(RegNo=regno).first()

        if user1:
            flash("Student Already Exist","warning")
            return render_template('/student.html')
        

        query=db.engine.execute(f"INSERT INTO `studentdetails` (`RegNo`,`Firstname`,`Lastname`,`Grade`,`ParentName`,`ContactDetails`,`DateofAdmission`,`AmountPaid`,`BatchNo`,`BatchStartDate`,`BatchTiming`) VALUES ('{regno}','{fname}','{lname}','{grade}','{parentname}','{contact}','{doa}','{amount}','{batchno}','{batchdate}','{batchtime}')")
        
    
        flash("Registered Succesfully","info")
        return redirect('/student')
        
     
    return render_template('student.html')


#For signup i.e signup.html
@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        name = request.form.get('Name')
        email = request.form.get('Email')
        password = request.form.get('Password')
        #print(username,email,password)
        user=Admin.query.filter_by(Email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        #used to insert values in db after signup
        new_user=db.engine.execute(f"INSERT INTO `admin` (`Name`,`Email`,`Password`) VALUES ('{name}','{email}','{encpassword}')")

        flash("Signup Successfully. Please Login","success")
        return render_template('login.html')    

    return render_template('signup.html')






#For login i.e login.html page

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form.get('Email')
        password = request.form.get('Password')
        #print(email,password)
        user=Admin.query.filter_by(Email=email).first()

        if user and check_password_hash(user.Password,password):
            login_user(user)
            # flash("Login Successful","primary")
            return redirect(url_for('student'))
        else:
            flash("Invalid Credentials","danger")
            return render_template('login.html')

    return render_template('login.html')



#For registered student
@app.route('/registered')
@login_required
def registered():
    query=db.engine.execute(f"SELECT * FROM `studentdetails`")
    return render_template('registered.html',query=query)
    




#For logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Successful","warning")
    return redirect(url_for('login'))


#For deleting account
@app.route('/deleteacc')
@login_required
def deleteacc():
    cid=current_user.id
    em=current_user.Email
    db.engine.execute(f"DELETE FROM `admin` WHERE `admin`.`id`= {cid} AND `admin`.`Email`= '{em}' ")
    return redirect(url_for('login'))


app.run(debug=True)     #For running this flask code
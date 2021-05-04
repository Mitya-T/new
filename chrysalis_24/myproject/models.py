# models.py
from flask import flash
from wtforms import ValidationError
from myproject import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from email_validator import validate_email, EmailNotValidError
from sqlalchemy_utils import PhoneNumberType
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#~~~~~~~~~~~~~~~~~ CREATING MODELS ~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~ USER class ~~~~~~~~~~~~~~~~~

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True) # only 64 characters
    last_name = db.Column(db.String(64), index=True) # only 64 characters
    dob = db.Column(db.String(64), index=True) # change to DATE!!!
    email = db.Column(db.String(64), unique=True, index=True) # only 64 characters, True - to prevent 2 different users with the same email!
    password_hash = db.Column(db.String(128), unique=True, index=True) # 128 characters - cause we need space for a HASHED password!
    address  = db.Column(db.String(64), index=True) # only 64 characters
    city = db.Column(db.String(64), index=True) # only 64 characters
    phone = db.Column(db.String(64), index=True) # change to DIGITS!!
    # phone = db.Column(PhoneNumberType())

    projects = db.relationship('Project',backref='author',lazy=True)



    def __init__ (self,first_name,last_name, dob, email, password, address, city, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.email = email
        self.password_hash = generate_password_hash(password) # cause we are saving the HASHED version, not the actual!
        self.address = address
        self.city = city
        self.phone = phone

    def __repr__(self):
        return f"User - {self.first_name}, {self.last_name}"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) # checks a new password against the hashed version

    def chk_pass(self, password):

        no_uppercase = False
        no_digit = False

        upper_count = 0
        number_count= 0

        if len(password) >= 8:
            for i in password:
                if i.isupper():
                    upper_count +=1
                elif i.isdigit():
                    number_count += 1

            if upper_count != 0 and number_count !=0:
                return True
            else:
                if upper_count == 0:
                    flash('Must contain UPPER CASE! Please try again...')
                elif number_count == 0:
                    flash('Must contain NUMBER! Please try again...')
                return False
        else:
            flash('Password must be at least 8 characters! Please try again...')
            return False



    def mel(self, email):
        try:
            # Validate.
            valid = validate_email(email)
            # Update with the normalized form.
            email = valid.email
            return  True
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            flash(str(e))
            return False


#~~~~~~~~~~~~~~~~~ PROJECT class ~~~~~~~~~~~~~~~~~


class Project(db.Model):
    __tablename__ = 'project'

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # means users.id is a ForeignKey for user_id

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # timestamp for a project publishing

    title = db.Column(db.String(140), nullable=False)  # Project TITLE
    text = db.Column(db.Text, nullable=False) # JUST A TEXT OF THE PROJECT
    language = db.Column(db.String(140), nullable=False) # JUST A TEXT OF THE PROJECT
    protocol = db.Column(db.String(140), nullable=False) # JUST A TEXT OF THE PROJECT
    format = db.Column(db.String(140), nullable=False) # JUST A TEXT OF THE PROJECT



    def __init__ (self,title,text,language,protocol,format,user_id):
        self.title = title
        self.text = text
        self.language = language
        self.protocol = protocol
        self.format = format

        self.user_id = user_id


        # def __init__ (self,parameter,protocol,format):
        #     self.parameter = parameter
        #     self.protocol = protocol
        #     self.format = format

    def __repr__(self):
        return f"Project ID: {self.id} --Date: {self.date} -- {self.title}"

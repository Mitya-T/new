# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, IntegerField, BooleanField, TextAreaField, SelectField, RadioField
from wtforms.fields.html5 import DateField, TelField
from wtforms.validators import DataRequired, Email, EqualTo, Length # to validate the data (
                                                # DataRequired --> NOT EMPTY,
                                                # Email --> using an email @. etc,
                                                # EqualTo-->pass confirm
                                                # Length --> Length of password)

from wtforms.widgets.html5 import TelInput
from wtforms import ValidationError # to check doubles in a DATABASE
import phonenumbers
from wtforms_alchemy import PhoneNumberField


class LoginForm(FlaskForm):

    email = StringField('Email (phone for mobile account)',validators=[DataRequired(),Email()], id='email')
    password = PasswordField('Password',validators=[DataRequired()], id='password')
    show_password = BooleanField('Show password', id='check')
    submit = SubmitField('Sign In!')



class RegistrationForm(FlaskForm):

    # Personal Information
    first_name = StringField('First Name:',validators=[DataRequired()], id='first')
    last_name = StringField('Last Name:',validators=[DataRequired()], id='last')
    # dob = StringField('Date of Birth: ', validators=[DataRequired()])
    dob = DateField('Date of Birth', format='%Y-%m-%d')


    # Account Information
    email = StringField('Email: ',validators=[DataRequired(),Email(message='You have an error'),EqualTo('email_confirm',message='Emails must match!')], id='email')
    email_confirm = StringField('Re-type Email: ', validators=[DataRequired()]) # so it has to match to EqualTo('email_confirm')
    password = PasswordField('Password: ',validators=[DataRequired(), Length(min=8, max=20, message='Password must contain more than 8 chars')], id='password')
    show_password = BooleanField('show password', id='check')


    # Contact Information
    address = StringField('Address: ',validators=[DataRequired()])
    city = StringField('City: ',validators=[DataRequired()])
    # phone = IntegerField('Phone: ',validators=[DataRequired()]) # this one is OK!
    # phone = TelField('Phone number', validators=[DataRequired()])
    phone = IntegerField('Phone', widget=TelInput())

    submit = SubmitField('Register!')

class PhoneForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    # submit = SubmitField('Submit')

    # def validate_phone(self, phone):
    #     try:
    #         p = phonenumbers.parse(phone.data)
    #         if not phonenumbers.is_valid_number(p):
    #             raise ValueError()
    #     except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
    #         raise ValidationError('Invalid phone number')


class ProjectForm(FlaskForm):

    title = StringField('Title of a project: ', validators=[DataRequired()])
    text = TextAreaField('Brief description: ', validators=[DataRequired()])
    # parameter = StringField('Parameter', validators=[DataRequired()])
    # protocol = StringField('Protocol', validators=[DataRequired()])
    # format = StringField('Format', validators=[DataRequired()])
    language = SelectField(u'Parameter: ',
                                        choices=[
                                        ('temperature', 'Temperature'),
                                        ('pressure', 'Pressure'),
                                        ('resistance', 'Resistance')])

    protocol = RadioField('Protocol: ', choices=[('LoRa','LoRa'),('bluetooth','Bluetooth')])
    format = SelectField(u'Format: ',
                                        choices=[
                                        ('portable', 'Portable'),
                                        ('desktop', 'Desktop'),
                                        ('other', 'Other'),
                                        ('not sure','Not Sure')])



    submit = SubmitField('Register a project!')









    # Validations for doubles (email and username)

    # def validate_email(self, email):
    #     if User.query.filter_by(email=self.email.data).first():
    #         raise ValidationError('Email has been registered')
    # def validate_username(self, username):
    #     if User.query.filter_by(username=self.username.data).first():
    #         raise ValidationError('Username has been registered')

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,PasswordField
from wtforms.validators import DataRequired, Length,EqualTo
class Loginform(FlaskForm):
    username=StringField('Name',validators=[DataRequired(),Length(min=2,max=30)])
    password=PasswordField('Password',validators=[DataRequired(), Length(min=4)])
    submit=SubmitField('Submit')
class Contactpage(FlaskForm):
    name=StringField('Name',validators=[DataRequired(),Length(min=2,max=50)])
    mail=StringField('Mail',validators=[DataRequired(),Length(min=5)])
    message=TextAreaField('Message',validators=[DataRequired(),Length(min=5)])
    submit=SubmitField('Submit')
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField('Email', validators=[DataRequired(), Length(min=6)])  # Removed Email()
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')
__author__ = 'Wei'

from flask_wtf import FlaskForm
from wtforms import FormField, StringField, PasswordField, SubmitField, TextAreaField, FileField, SelectField, SelectMultipleField, DateField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Regexp
from app.models import Admin, Tag, Auth, Role, User
from flask import session

class RegistForm(FlaskForm):
    '''User register form'''
    name = StringField(
        label = 'Username',
        validators = [
            DataRequired('Please input the username')
        ],
        description = 'username',
        render_kw = {
            'class' : 'form-control input-lg',
            'placeholder': 'username',
            'required':'required'
        }
    )
    email = StringField(
        label = 'Email',
        validators = [
            DataRequired('Please input the email'),
            Email('Email format is not right')
        ],
        description = 'email',
        render_kw = {
            'class': 'form-control input-lg',
            'placeholder':'email',
            'required':'required'
        }
    )
    phone = StringField(
        label = 'Phone',
        validators=[
            DataRequired('Please input the mobile phone no.'),
            Regexp('\\d{10}',message='The phone format is not right')
        ],
        description = 'phone',
        render_kw={
            'class':'form-control input-lg',
            'placeholder':'phone',
            'required':'required'
        }
    )
    pwd = PasswordField(
        label = 'Password',
        validators=[
            DataRequired('Please input the password')
        ],
        description='password',
        render_kw={
            'class':'form-control input-lg',
            'placeholder': 'password',
            'required':'required'
        }
    )

    repwd = PasswordField(
        label = 'Confirm Password',
        validators = [
            DataRequired('Please input the confirm password'),
            EqualTo('pwd','The confirm password does not match')
        ],
        description = 'condirm password',
        render_kw = {
            'class':'form-control input-lg',
            'placeholder':'condirm password',
            'required':'required'
        }
    )

    submit = SubmitField(
        'Register',
        render_kw={
            'class':'btn btn-lg btn-success btn-block'
        }
    )

    def validata_name(self,field):
        '''check if the username exists'''
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError('This username has existed')

    def validata_email(self, field):
        '''Check if the email exists'''
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError('This email has existed')   

    def validata_phone(self,field):
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user == 1:
            raise ValidationError('The phone number has existed')  

class LoginForm(FlaskForm):
    '''User login form'''
    name = StringField(
        label = 'Username',
        validators = [
            DataRequired('Please input the username')
        ],
        description = 'username',
        render_kw={
            'class':'form-control input-lg',
            'placeholder':'username',
            'required':'required'
        }
    ) 
    pwd = PasswordField(
        label = 'Password',
        validators = [
            DataRequired('Please inpout password')
        ],
        description = 'password',
        render_kw={
            'class':'form-control input-lg',
            'placeholder':'password',
            'required':'required'
        }
    )                      
    submit = SubmitField(
        'Login',
        render_kw={
            'class': 'btn btn-lg btn-success btn-block'
        }
    )
'''
class KnowForm(FlaskForm):
    User Analyze Form
    DOB = DateField(
        label = 'birthday',
        validators = [
            DataRequired('Please input your birthday')
        ],
        description = 'birthday',
        render_kw={
            'class':'form-control input-lg',
            'placeholder':'birthday',
            'required':'required'
        }
    ) 
    social = StringField(
        label = 'social',
        validators = [
            DataRequired('Please inpout social')
        ],
        description = 'password',
        render_kw={
            'class':'form-control input-lg',
            'placeholder':'social',
            'required':'required'
        }
    )                      
    submit = SubmitField(
        'Know',
        render_kw={
            'class': 'btn btn-lg btn-success btn-block'
        }
    )    
'''
class UserdetailForm(FlaskForm):
    '''user eidt info form'''
    name = StringField(
        label = 'Username',
        validators = [
            DataRequired('Please input username'),
        ],
        description = 'username',
        render_kw={
            'class':'form-control'
        }
    )  
    dob = StringField(
        label = 'Birthday',
        validators = [
            DataRequired('Please input your birthday'),
        ],
        description = 'birthday',
        render_kw={
            'class':'form-control',
            'id': 'input_dob',
            'placeholder':'please fill your birthday'
        }
    )  
    gender = SelectField(
        label = 'Gender',
        validators = [
            DataRequired('Please choose your gender'),
        ],
        coerce = int,
        choices = [(1,'Male'),(2,'Female')],
        description = 'gender',
        render_kw={
            'class':'form-control',
            'placeholder':'please fill your gender'
        }
    )    
    email = StringField(
        label = 'Email',
        validators=[
            DataRequired('Please input email'),
            Email('Email format is not right')
        ],
        description = 'Email',
        render_kw={
            'class':'form-control'
        }
    )
    phone = StringField(
        label = 'Phone',
        validators=[
            DataRequired('Please input the phone no.'),
            Regexp('\\d{10}', message='The phone format is not right')
        ],
        description='phone',
        render_kw = {
            'class':'form-control'
        }
    )
    facebook = StringField(
        label = 'Facebook',
        validators = [
            DataRequired('Please input your facebook url'),
        ],
        description = 'facebook',
        render_kw={
            'class':'form-control',
            'placeholder':'Please input your facebook url'
        }
    )  
    instagram = StringField(
        label = 'Instagram',
        validators = [
            DataRequired('Please input your instagram url'),
        ],
        description = 'instagram',
        render_kw={
            'class':'form-control',
            'placeholder':'Please input your instagram url'
        }
    )  
    twitter = StringField(
        label = 'Twitter',
        validators = [
            DataRequired('Please input your twitter url'),
        ],
        description = 'twitter',
        render_kw={
            'class':'form-control',
             'placeholder':'Please input your twitter url'
        }
    )  
    face = FileField(
        label = 'Profile',
        description = 'profile'
    )
    info = TextAreaField(
        label = 'Introduction',
        description='introduction',
        render_kw = {
            'class':'form-control',
            'rows':10
        }
    )
    submit = SubmitField(
        'Save modification',
        render_kw = {
            'class' : 'btn btn-success'
        }
    )

class PwdForm(FlaskForm):
    '''Modify user password form'''
    old_pwd = PasswordField(
        label='old password',
        validators = [
            DataRequired('Please input the old password'),
        ],
        description = 'old password',
        render_kw = {
            'class':'form-control',
            'placeholder':'old password',
            'required':'required'
        }
    )
    new_pwd = PasswordField(
        label = 'new password',
        validators = [
            DataRequired('Please input the new password'),
        ],
        description='new password',
        render_kw = {
            'class':'form-control',
            'placeholder':'new password',
            'required':'required'
        }
    )
    submit = SubmitField(
        'Modify password',
        render_kw={
            'class':'btn btn-success'
        }
    )


class CommentForm(FlaskForm):
    '''Movie comment form'''
    content = TextAreaField(
        label = 'comment content',
        description = 'content',
        validators=[
            DataRequired('Please input comment content')
        ],
        render_kw={
            'id':'comment',
            'rows':5
        }
    )
    submit = SubmitField(
        'submit comment',
        render_kw = {
            'class':'btn btn-success',
            'id':'btn-sub',
        }
    )
#!/user/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Wei'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError,EqualTo
from app.models import Admin, Tag, Auth, Role
from flask import session

tags = Tag.query.order_by(Tag.name).all()
auth_list = Auth.query.all()
role_list = Role.query.all()

class LoginForm(FlaskForm):
    '''Admin login form'''
    account = StringField(
        label = 'Account',
        validators = [
            DataRequired('Please input your account')
        ],
        description='account',
        render_kw={
            'class':'form-control',
            'placeholder':'Please input your account',
            'required': 'required'
        }
    )

    pwd = PasswordField(
        label = 'Password',
        validators = [
            DataRequired('Please input your password')
        ],
        description='password',
        render_kw={
            'class':'form-control',
            'placeholder':'Please input your password',
            'required':'required'
        }
    )

    submit = SubmitField(
        'Login',
        render_kw={
            'class':'btn btn-primary btn-block btn-flat'
        }
    )

    def validate_account(self, field):
        '''validate if the account exists'''
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError('your account does not exist, please check it') 


class TagForm(FlaskForm):
    '''Movie tag form'''
    name = StringField(
        label = 'Tag name',
        validators = [
            DataRequired('Please input the tag name')
        ],
        description = 'Tag',
        render_kw = {
            'class':'form-control',
            'placeholder':'Please input tag name!',
            'required':'required'
        }
    )

    zodiac = SelectMultipleField(
        label = 'Related Zodiac',
        validators = [
            DataRequired('Please choose the related zodiac')
        ],
        coerce = int,
        choices = [(1,'Aquarius'),(2,'Pisces'),(3,'Aries'),(4,'Taurus'),(5,'Gemini'),(6,'Cancer'),(7,'Leo'),(8,'Virgo'),(9,'Libra'),(10,'Scorpio'),(11,'Sagittarius'),(12,'Capricorn')],
        description = 'zodiac',
        render_kw = {
            'class': 'form-control',
        }
    )
    
    submit = SubmitField(
        'submit',
        render_kw={
            'class':'btn btn-primary'
        }
    )

class MovieForm(FlaskForm):
    '''Movie managment form'''
    title = StringField(
        label = 'Video Name',
        validators = [
            DataRequired('Please input movie name')
        ],
        description = 'movie name',
        render_kw={
            'class':'form-control',
            'placeholder':'Please input the movie name',
            'required':'required'
        }
    )

    url = FileField(
        label = 'File',
        description = 'file'
    )

    info = TextAreaField(
        label = 'Introduction',
        validators = [
            DataRequired('Please input the introduction')
        ],
        description = 'introduction',
        render_kw={
            'class':'form-control',
            'rows':'10'
        }
    )

    logo = FileField(
        label = 'Cover',
        description = 'Cover',
    )

    star = SelectField(
        label = 'Star',
        validators=[
            DataRequired('Please choose the star')
        ],
        coerce = int,
        choices = [(1,'1 star'),(2,'2 stars'),(3,'3 stars'),(4,'4 stars'),(5,'5 stars')],
        description = 'star',
        render_kw={
            'class':'form-control',
        }
    )

    tags = SelectMultipleField(
        label = 'Tags',
        validators = [
            DataRequired('Please choose the tag')
        ],
        coerce = int,
        choices = [(v.id, v.name) for v in tags],
        description = 'tag',
        render_kw = {
            'class': 'form-control',
        }
    )

    area = StringField(
        label = 'Place',
        validators=[
            DataRequired('Please input the place')
        ],
        description = 'place of origin',
        render_kw ={
            'class': 'form-control',
            'placeholder':'please input the place',
            'required':'required'
        }
    )

    length = StringField(
        label = 'Video Length',
        validators =[
            DataRequired('Please input the movie length')
        ],
        description = 'movie length',
        render_kw = {
            'class': 'form-control',
            'placeholder':'please input the movie length(minutes)',
            'required':'required'
        }
    )

    release_time = StringField(
        label = 'Release Time',
        validators =[
            DataRequired('Please input the release time')
        ],
        description = 'release time',
        render_kw = {
            'class': 'form-control',
            'id': 'input_release_time',
            'placeholder':'please choose the release time',
            'required':'required'
        }
    )
    submit = SubmitField(
        'submit',
        render_kw={
            'class':'btn btn-primary',
        }
    )


class MusicForm(FlaskForm):
    '''Music managment form'''
    title = StringField(
        label = 'Music Name',
        validators = [
            DataRequired('Please input music name')
        ],
        description = 'music name',
        render_kw={
            'class':'form-control',
            'placeholder':'Please input the music name',
            'required':'required'
        }
    )

    url = FileField(
        label = 'File',
        description = 'file'
    )

    info = TextAreaField(
        label = 'Introduction',
        validators = [
            DataRequired('Please input the introduction')
        ],
        description = 'introduction',
        render_kw={
            'class':'form-control',
            'rows':'10'
        }
    )

    logo = FileField(
        label = 'Cover',
        description = 'Cover',
    )

    star = SelectField(
        label = 'Star',
        validators=[
            DataRequired('Please choose the star')
        ],
        coerce = int,
        choices = [(1,'1 star'),(2,'2 stars'),(3,'3 stars'),(4,'4 stars'),(5,'5 stars')],
        description = 'star',
        render_kw={
            'class':'form-control',
        }
    )

    tags = SelectMultipleField(
        label = 'Tags',
        validators = [
            DataRequired('Please choose the tag')
        ],
        coerce = int,
        choices = [(v.id, v.name) for v in tags],
        description = 'tag',
        render_kw = {
            'class': 'form-control',
        }
    )

    singer = StringField(
        label = 'Singer',
        validators=[
            DataRequired('Please input the singer')
        ],
        description = 'singer of music',
        render_kw ={
            'class': 'form-control',
            'placeholder':'please input the singer',
            'required':'required'
        }
    )

    length = StringField(
        label = 'Music Length',
        validators =[
            DataRequired('Please input the music length')
        ],
        description = 'music length',
        render_kw = {
            'class': 'form-control',
            'placeholder':'please input the music length(minutes)',
            'required':'required'
        }
    )

    release_time = StringField(
        label = 'Release Time',
        validators =[
            DataRequired('Please input the release time')
        ],
        description = 'release time',
        render_kw = {
            'class': 'form-control',
            'id': 'input_release_time',
            'placeholder':'please choose the release time',
            'required':'required'
        }
    )
    submit = SubmitField(
        'submit',
        render_kw={
            'class':'btn btn-primary',
        }
    )    


class BookForm(FlaskForm):
    '''Book managment form'''
    title = StringField(
        label = 'Book Name',
        validators = [
            DataRequired('Please input book name')
        ],
        description = 'book name',
        render_kw={
            'class':'form-control',
            'placeholder':'Please input the book name',
            'required':'required'
        }
    )

    url = StringField(
        label = 'Book Link',
        validators = [
            DataRequired('Please input the book link')
        ],
        description = 'book link',
        render_kw={
            'class':'form-control',
            'placeholder':'Please input the book link',
            'required':'required'
        }
    )

    info = TextAreaField(
        label = 'Introduction',
        validators = [
            DataRequired('Please input the introduction')
        ],
        description = 'introduction',
        render_kw={
            'class':'form-control',
            'rows':'10'
        }
    )

    logo = FileField(
        label = 'Cover',
        description = 'Cover',
    )

    star = SelectField(
        label = 'Star',
        validators=[
            DataRequired('Please choose the star')
        ],
        coerce = int,
        choices = [(1,'1 star'),(2,'2 stars'),(3,'3 stars'),(4,'4 stars'),(5,'5 stars')],
        description = 'star',
        render_kw={
            'class':'form-control',
        }
    )

    tags = SelectMultipleField(
        label = 'Tags',
        validators = [
            DataRequired('Please choose the tag')
        ],
        coerce = int,
        choices = [(v.id, v.name) for v in tags],
        description = 'tags',
        render_kw = {
            'class': 'form-control',
        }
    )

    author = StringField(
        label = 'Author',
        validators=[
            DataRequired('Please input the author')
        ],
        description = 'place of origin',
        render_kw ={
            'class': 'form-control',
            'placeholder':'please input the author',
            'required':'required'
        }
    )

    release_time = StringField(
        label = 'Time',
        validators =[
            DataRequired('Please input the release time')
        ],
        description = 'release time',
        render_kw = {
            'class': 'form-control',
            'id': 'input_release_time',
            'placeholder':'please choose the release time',
            'required':'required'
        }
    )
    submit = SubmitField(
        'submit',
        render_kw={
            'class':'btn btn-primary',
        }
    )    


class PreviewForm(FlaskForm):
    '''movie preview management form'''
    title = StringField(
        label='Preview Title',
        validators = [
            DataRequired('Please input preview title')
        ],
        description ='Preview title',
        render_kw={
            'class' : 'form-control',
            'placeholder':'Please input preview title',
            'required':'required'
        }
    )

    logo = FileField(
        label = 'Preview Cover',
        validators =[
            DataRequired('Please upload the preview cover')
        ],
        description = 'preview cover'
    ) 
    submit = SubmitField(
        'submit',
        render_kw={
            'class':'btn btn-primary',
        }
    )

class PwdForm(FlaskForm):
    '''Modify admin password form'''
    old_pwd = PasswordField(
        label = 'Old Password',
        validators=[
            DataRequired('Please input old password')
        ],
        description = 'old password',
        render_kw = {
            'class':'form-control',
            'placeholder':'please input the old password',
            'required':'required'
        }
    )

    new_pwd = PasswordField(
        label = 'New Password',
        validators = [
            DataRequired('Please input the new password')
        ],
        description = 'new password',
        render_kw ={
            'class': 'form-control',
            'placeholder': 'Please input the new password',
            'required': 'required' 
        }
    )

    submit = SubmitField(
        'Modify',
        render_kw = {
            'class' : 'btn btn-primary'
        }
    )

    def validate_old_pwd(self, field):
        '''validate if the old passsword is right'''
        pwd = field.data
        name = session['admin']
        admin = Admin.query.filter_by(
            name = name
        ).first()
        admin.check_pwd(pwd)
        if not admin.check_pwd(pwd):
            raise ValidationError('Input the wrong old password, please input again')

class AuthForm(FlaskForm):
    '''authority form'''
    name = StringField(
        label = 'Authority Name',
        validators = [
            DataRequired('Please input authority name')
        ],
        description = 'authority name',
        render_kw = {
            'class':'form-control',
            'placeholder':'please input authority name',
            'required':'required'
        }
    )
    url = StringField(
        label = 'Authority Url',
        validators = [
            DataRequired('Please input authority url')
        ],
        description = 'authority url',
        render_kw ={
            'class':'form-control',
            'placeholder':'please input authority url',
            'required':'required'
        }
    )
    submit = SubmitField(
        'submit',
        render_kw ={
            'class':'btn btn-primary'
        }
    )

class RoleForm(FlaskForm):
    '''Role form'''
    name = StringField(
        label = 'Role Name',
        validators = [
            DataRequired('Please input role name')
        ],
        description = 'role name',
        render_kw = {
            'class' : 'form-control',
            'placeholder' : 'Please input role name',
            'required' : 'required'
        }
    )
    auths = SelectMultipleField(
        label = 'Authority List',
        validators = [
            DataRequired('Please choose operate authority')
        ],
        coerce = int,
        choices = [(v.id, v.name) for v in auth_list],
        description = 'authority list',
        render_kw={
            'class': 'form-control',
            'required': 'required'
        }
    )
    submit = SubmitField(
        'submit',
        render_kw={
            'class':'btn btn-primary'
        }
    )

class AdminForm(FlaskForm):
    '''Admin register form'''
    name = StringField(
        label = 'Admin Name',
        validators=[
            DataRequired('Please input admin name')
        ],
        description = 'Admin Name',
        render_kw = {
            'class': 'form-control',
            'placeholder': 'please input admin name',
            'required': 'required'
        }
    )
    pwd = PasswordField(
        label = 'Admin Password',
        validators=[
            DataRequired('Please input admin password')
        ],
        description='Admin Password',
        render_kw = {
            'class': 'form-control',
            'placeholder': 'Please input admin password',
            'required' : 'required'
        }
    )    
    repwd = PasswordField(
        label = 'Admin Password Confirm',
        validators = [
            DataRequired('Please input admin confirm password'),
            EqualTo('pwd', message='The confirm password is not cosistent')
        ],
        description = 'admin confirm password',
        render_kw = {
            'class': 'form-control',
            'placeholder': 'Please input admin confirm password',
            'required': 'required'
        }
    )
    role_id = SelectField(
        label = 'Role',
        validators = [
            DataRequired('Please tick the role')
        ],
        coerce = int,
        choices = [(v.id, v.name) for v in role_list],
        description = 'role',
        render_kw = {
            'class': 'form-control',
            'required': 'required'
        }
    )
    submit = SubmitField(
        'submit',
        render_kw={
            'class': 'btn btn-primary'
        }
    )



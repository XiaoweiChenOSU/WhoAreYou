#!/user/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Wei'

from app import db
from datetime import datetime

#user model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    gender = db.Column(db.Integer)
    pwd = db.Column(db.String(100))
    DOB = db.Column(db.Date)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text)
    face = db.Column(db.String(255))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    uuid = db.Column(db.String(255), unique=True)
    facebook = db.Column(db.String(255))
    instagram = db.Column(db.String(255))
    twitter = db.Column(db.String(255))


    userlogs = db.relationship('Userlog', backref='user')
    comments = db.relationship('Comment', backref='user')
    moviecols = db.relationship('Moviecol', backref='user')
    musiccols = db.relationship('Musiccol', backref='user')
    bookcols = db.relationship('Bookcol', backref='user')

    def __repr__(self):
        return '<User %r>' % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)

#userloginlog
class Userlog(db.Model):
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default= datetime.now)

    def __repr__(self):
        return '<Userlog %r>' % self.id


#constellation
'''
class Constellation(db.Model):
    __tablename__ = 'constellation'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    startdate = db.Column(db.DateTime, index=True)
    enddate = db.Column(db.DateTime, index=True)


    users = db.relationship('User', backref='constellation')


    def __repr__(self):
        return '<Constellation %r>' % self.id 
'''

#tag
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    zodiac = db.Column(db.String(250))
    addtime = db.Column(db.DateTime, index= True, default=datetime.now)

    def __repr__(self):
        return '<Tag %r>' % self.name

#movie
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)
    logo = db.Column(db.String(255), unique=True)
    star = db.Column(db.SmallInteger)
    playnum = db.Column(db.BigInteger)
    commentnum = db.Column(db.BigInteger)
    tags = db.Column(db.String(100))
    area = db.Column(db.String(255))
    release_time = db.Column(db.Date)
    length = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    comments = db.relationship('Comment', backref='movie')
    moviecols = db.relationship('Moviecol', backref='movie')

    def __repr__(self):
        return '<Movie %r>' % self.title

#music
class Music(db.Model):
    __tablename__ = 'music'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)
    logo = db.Column(db.String(255), unique=True)
    star = db.Column(db.SmallInteger)
    playnum = db.Column(db.BigInteger)
    commentnum = db.Column(db.BigInteger)
    tags = db.Column(db.String(100))
    singer = db.Column(db.String(255))
    release_time = db.Column(db.Date)
    length = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    comments = db.relationship('Comment', backref='music')
    musiccols = db.relationship('Musiccol', backref='music')

    def __repr__(self):
        return '<Music %r>' % self.title        

#book
class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)
    logo = db.Column(db.String(255), unique=True)
    star = db.Column(db.SmallInteger)
    commentnum = db.Column(db.BigInteger)
    tags = db.Column(db.String(100))
    author = db.Column(db.String(255))
    release_time = db.Column(db.Date)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    comments = db.relationship('Comment', backref='book')
    bookcols = db.relationship('Bookcol', backref='book')

    def __repr__(self):
        return '<Book %r>' % self.title        



#movie trailer 
class Preview(db.Model):
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Preview %r>' % self.title

#movie comment
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    music_id = db.Column(db.Integer, db.ForeignKey('music.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Comment %r>' % self.id

#Movie Collection
class Moviecol(db.Model):
    __tablename__ = 'moviecol'
    id = db.Column(db.Integer, primary_key= True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Moviecol %r>' %self.id


#Music Collection
class Musiccol(db.Model):
    __tablename__ = 'musiccol'
    id = db.Column(db.Integer, primary_key= True)
    music_id = db.Column(db.Integer, db.ForeignKey('music.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Musiccol %r>' %self.id


#Book Collection
class Bookcol(db.Model):
    __tablename__ = 'bookcol'
    id = db.Column(db.Integer, primary_key= True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Bookcol %r>' %self.id        


#Define role authority
class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Auth %r>' % self.name

#role create
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    auths = db.Column(db.String(600))
    addtime = db.Column(db.DateTime,index=True, default=datetime.now)
    
    admins = db.relationship('Admin', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

#manager create
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.SmallInteger)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    adminlogs = db.relationship('Adminlog', backref='admin')
    oplogs = db.relationship('Oplog', backref='admin')

    def __repr__(self):
        return '<Admin %r>' % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd) 

#Manager Login log
class Adminlog(db.Model):
    __tablename__ = 'adminlog'
    id = db.Column(db.Integer,primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Adminlog %r>' %self.id

#manager operation log
class Oplog(db.Model):
    __tablename__ = 'oplog'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Oplog %r>' % self.id


#movie
class Know(db.Model):
    __tablename__ = 'know'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    zodiac = db.Column(db.String(50))
    chineseZodiac = db.Column(db.String(50))
    strengths =  db.Column(db.String(300))
    weaknesses =  db.Column(db.String(300))
    jobs = db.Column(db.String(300))
    luckNum = db.Column(db.String(30))
    luckColor = db.Column(db.String(300))
    luckFlower = db.Column(db.String(300))
    luckDirection = db.Column(db.String(300))
    likes = db.Column(db.String(300))
    dislikes = db.Column(db.String(300))
    zodiac_info = db.Column(db.Text)
    chineseZodiac_info = db.Column(db.Text)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Know %r>' % self.id

   

'''
if __name__ == '__main__':

    db.drop_all()
    db.create_all()
    print('---------------Successful-----------------')
    role = Role(
        name = 'Super Admin',
        auths = ''
    )
    db.session.add(role)
    db.session.commit()
    

    from werkzeug.security import generate_password_hash
    admin = Admin(
        name = 'xiaowei',
        pwd = generate_password_hash('xiaowei'),
        is_super = 0,
        role_id = 1
    )
    db.session.add(admin)
    db.session.commit()

'''    










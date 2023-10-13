# !/user/bin/env python
# -*- coding:utf-8 -*- 
# time: 2018/3/7--19:50
__author__ = 'Wei'

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1:3306/movie'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/FinalProject'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)),'static/uploads/') #Define the save path of files uploaded in the background
app.config['FC_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)),'static/uploads/users/') #Define the save path of the user avatar file uploaded in the foreground

app.debug = False #Development debug mode

# app.config['SECRET_KEY'] = 'Wei'
app.secret_key = 'Wei' #key:For csrf encryption

db = SQLAlchemy(app)
from app import models


'''
db.drop_all()
db.create_all()

role = models.Role(
    name = 'Super Admin',
    auths = '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44'
)
db.session.add(role)
db.session.commit()

auth_1 = models.Auth( id = 1, name='tag_add', url='/admin/tag/add/', addtime='2019-06-06 12:37:01')
auth_2 = models.Auth( id = 2, name='tag_list', url='/admin/tag/list/<int:page>/', addtime='2019-06-06 12:37:01')
auth_3 = models.Auth( id = 3, name='tag_del', url='/admin/tag/del/<int:id>/', addtime='2019-06-06 12:37:01')
auth_4 = models.Auth( id = 4, name='tag_edit', url='/admin/tag/edit/<int:id>/', addtime='2019-06-06 12:37:01')
auth_5 = models.Auth( id = 5, name='movie_add', url='/admin/movie/add/', addtime='2019-06-06 12:37:01')
auth_6 = models.Auth( id = 6, name='movie_list', url='/admin/movie/list/<int:page>/', addtime='2019-06-06 12:37:01')
auth_7 = models.Auth( id = 7, name='movie_del', url='/admin/movie/del/<int:id>/', addtime='2019-06-06 12:37:01')
auth_8 = models.Auth( id = 8, name='movie_edit', url='/admin/movie/edit/<int:id>/', addtime='2019-06-06 12:37:01')
auth_9 = models.Auth( id = 9, name='preview_add', url='/admin/preview/add/', addtime='2019-06-06 12:37:01')
auth_10 = models.Auth( id = 10, name='preview_list', url='/admin/preview/list/<int:page>/', addtime='2019-06-06 12:37:01')
auth_11 = models.Auth( id = 11, name='preview_del', url='/admin/preview/del/<int:id>/', addtime='2019-06-06 12:37:01')
auth_12 = models.Auth( id = 12, name='preview_edit', url='/admin/preview/edit/<int:id>/', addtime='2019-06-06 12:37:01')
auth_13 = models.Auth( id = 13, name='user_list', url='/admin/user/list/<int:page>/', addtime='2019-06-06 12:37:01')
auth_14 = models.Auth( id = 14, name='user_view', url='/admin/user/view/<int:id>/', addtime='2019-06-06 12:37:01')
auth_15 = models.Auth( id = 15, name='user_del', url='/admin/user/del/<int:id>/', addtime='2019-06-06 12:37:01')
auth_16 = models.Auth( id = 16, name='admin_add', url='/admin/admin/add/', addtime='2019-06-06 12:37:01')
auth_17 = models.Auth( id = 17, name='admin_list', url='/admin/admin/list/<int:page>/', addtime='2019-06-06 12:37:01')
auth_18 = models.Auth( id = 18, name='comment_list', url='/admin/comment/list/<int:page>/', addtime='2019-06-06 12:37:01')
auth_19 = models.Auth( id = 19, name='comment_del', url='/admin/comment/del/<int:id>/', addtime='2019-06-06 12:37:01')
auth_20 = models.Auth( id = 20, name='moviecol_list', url='/admin/moviecol/list/<int:page>/', addtime='2019-06-06 12:37:01')
auth_21 = models.Auth( id = 21, name='moviecol_del', url='/admin/moviecol/del/<int:id>/', addtime='2019-06-06 12:37:01')
auth_22 = models.Auth( id = 22, name='oplog_list', url='/admin/oplog/list/<int:page>/', addtime='2019-06-06 12:37:01')
auth_23 = models.Auth( id = 23, name='adminloginlog_list', url='/admin/adminloginlog/list/<int:page>/', addtime='2019-06-06 12:37:01')
auth_24 = models.Auth( id = 24, name='userloginlog_list', url='/admin/userloginlog/list/<int:page>/', addtime='2019-06-06 12:37:01')
auth_25 = models.Auth( id = 25, name='auth_add', url='/admin/auth/add/', addtime='2019-06-06 12:37:01')
auth_26 = models.Auth( id = 26, name='auth_list', url='/admin/auth/list/<int:page>/', addtime='2019-06-06 12:37:01')
auth_27 = models.Auth( id = 27, name='auth_del', url='/admin/auth/del/<int:id>/', addtime='2019-06-06 12:37:01')
auth_28 = models.Auth( id = 28, name='auth_edit', url='/admin/auth/edit/<int:id>/', addtime='2019-06-06 12:37:01')
auth_29 = models.Auth( id = 29, name='role_add', url='/admin/role/add/', addtime='2019-06-06 12:37:01')
auth_30 = models.Auth( id = 30, name='role_list', url='/admin/role/list/<int:page>/', addtime='2019-06-06 12:37:01')
auth_31 = models.Auth( id = 31, name='role_del', url='/admin/role/del/<int:id>/', addtime='2019-06-06 12:37:01')
auth_32 = models.Auth( id = 32, name='role_edit', url='/admin/role/edit/<int:id>/', addtime='2019-06-06 12:37:01')
auth_33 = models.Auth( id = 33, name='music_add', url='/admin/music/add/', addtime='2019-06-06 12:37:01')
auth_34 = models.Auth( id = 34, name='music_list', url='/admin/music/list/<int:page>/', addtime='2019-06-06 12:37:01')
auth_35 = models.Auth( id = 35, name='music_del', url='/admin/music/del/<int:id>/', addtime='2019-06-06 12:37:01')
auth_36 = models.Auth( id = 36, name='music_edit', url='/admin/music/edit/<int:id>/', addtime='2019-06-06 12:37:01')
auth_37 = models.Auth( id = 37, name='book_add', url='/admin/book/add/', addtime='2019-06-06 12:37:01')
auth_38 = models.Auth( id = 38, name='book_list', url='/admin/book/list/<int:page>/', addtime='2019-06-06 12:37:01')
auth_39 = models.Auth( id = 39, name='book_del', url='/admin/book/del/<int:id>/', addtime='2019-06-06 12:37:01')
auth_40 = models.Auth( id = 40, name='book_edit', url='/admin/book/edit/<int:id>/', addtime='2019-06-06 12:37:01')
auth_41 = models.Auth( id = 41, name='musiccol_list', url='/admin/musiccol/list/<int:page>/', addtime='2019-06-06 12:37:01')
auth_42 = models.Auth( id = 42, name='musiccol_del', url='/admin/musiccol/del/<int:id>/', addtime='2019-06-06 12:37:01')
auth_43 = models.Auth( id = 43, name='bookcol_list', url='/admin/bookcol/list/<int:page>/', addtime='2019-06-06 12:37:01')
auth_44 = models.Auth( id = 44, name='bookcol_del', url='/admin/bookcol/del/<int:id>/', addtime='2019-06-06 12:37:01')



db.session.add_all([auth_1, auth_2, auth_3, auth_4, auth_5, auth_6, auth_7, auth_8, auth_9,auth_10, auth_11, auth_12, auth_13, auth_14, auth_15, auth_16, auth_17, auth_18, auth_19, auth_20, auth_21, auth_22, auth_23, auth_24, auth_25, auth_26, auth_27, auth_28, auth_29, auth_30, auth_31, auth_32,auth_33, auth_34, auth_35, auth_36, auth_37, auth_38, auth_39, auth_40, auth_41, auth_42, auth_43, auth_44])
db.session.commit()



pre_1 = models.Preview( id = 1, title = 'Spring', logo = '20190625161310ea88f7f50f9a4bba83e7c4f6b5702b19.jpg', addtime= '2019-06-25 16:13:11')
pre_2 = models.Preview( id = 2, title = 'Star', logo = '20190625161349a6755e6a6b984336b86ee16768aa154e.jpg', addtime= '2019-06-25 16:13:11')
pre_3 = models.Preview( id = 3, title = 'Winter', logo = '20190625161400201574cbbd6341b0982cdb7d6a212cd4.jpg', addtime= '2019-06-25 16:13:11')
pre_4 = models.Preview( id = 4, title = 'Flowers', logo = '201906251614148742208c906d4d73951e9ce2274dd8a3.jpg', addtime= '2019-06-25 16:13:11')
pre_5 = models.Preview( id = 5, title = 'Friends', logo = '20190625161432a792516e53c24b8aabdba8a550649add.jpg', addtime= '2019-06-25 16:13:11')
pre_6 = models.Preview( id = 6, title = 'Book', logo = '201906251615322e9f2899568c4f4999eb8366a25f9962.jpg', addtime= '2019-06-25 16:13:11')

db.session.add_all([pre_1, pre_2, pre_3, pre_4, pre_5, pre_6])
db.session.commit()


tag_1 = models.Tag(id = 1, name = 'comedy')
tag_2 = models.Tag(id = 2, name = 'tragedy')
tag_3 = models.Tag(id = 3, name = 'fiction')

db.session.add_all([tag_1, tag_2, tag_3])
db.session.commit()





from werkzeug.security import generate_password_hash
admin = models.Admin(
    name = 'xiaowei',
    pwd = generate_password_hash('xiaowei'),
    is_super = 0,
    role_id = 1
)
db.session.add(admin)
db.session.commit()

'''

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)

app.register_blueprint(admin_blueprint, url_prefix='/admin')


# 404 page
@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html'), 404

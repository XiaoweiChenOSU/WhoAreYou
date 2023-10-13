#!/user/bin/env python
#-*- coding:utf-8 -*-
#time: 2019/6/7 -- 19:52

__author__ = 'Wei'

from . import admin
from flask import render_template, url_for, redirect, flash, session, request, abort
from app.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm, PwdForm, AuthForm, RoleForm, AdminForm, MusicForm, BookForm
from app.models import Admin, Tag, Movie, Preview, User, Comment, Moviecol, Oplog, Adminlog, Userlog, Auth, Role, Music, Book, Musiccol, Bookcol
from werkzeug.utils import secure_filename
from functools import wraps 
from app import db, app
import os, stat
import uuid
import datetime
from werkzeug.security import generate_password_hash
import math

@admin.context_processor
def tpl_extra():
    data = dict(
        online_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    return data

def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function        

def admin_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin = Admin.query.join(
            Role
        ).filter(
            Role.id == Admin.role_id,
            Admin.id == session['admin_id']
        ).first()
        auths = admin.role.auths
        auths = list(map(lambda v: int(v), auths.split(',')))
        auth_list = Auth.query.all()
        urls = [v.url for v in auth_list for val in auths if val==v.id]
        rule = request.url_rule
        if str(rule) not in urls:
            abort(404)
        return f(*args, **kwargs)
    return decorated_function


def change_filename(filename): 
    fileinfo = filename.split('.')
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex)+'.'+fileinfo[-1]
    return filename

@admin.route('/')
@admin_login_req
@admin_auth
def index():
    return render_template('admin/index.html')


@admin.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data['account']).first()
        if not admin.check_pwd(data['pwd']):
            flash('Password is not right', 'err')
            return redirect(url_for('admin.login'))
        session['admin'] = data['account']
        session['admin_id'] = admin.id
        adminlog = Adminlog(
            admin_id = session['admin_id'],
            ip = request.remote_addr,
            reason = 'login'
        )
        db.session.add(adminlog)
        db.session.commit()
        return redirect(request.args.get('next') or url_for('admin.tag_add')) 
    return render_template('admin/login.html', form=form)

@admin.route('/logout/')
@admin_login_req
def logout():
    session.pop('admin', None)
    session.pop('admin_id', None)
    return redirect(url_for('admin.login'))


@admin.route('/pwd/', methods=['GET','POST'])
@admin_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=session['admin']).first()
        admin.pwd = generate_password_hash(data['new_pwd'])
        db.session.add(admin)
        db.session.commit()
        flash('Modify password successfully, please login again', 'ok')
        return redirect(url_for('admin.logout'))
    return render_template('admin/pwd.html', form=form)

@admin.route('/tag/add/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data['name']).count()
        if tag == 1:
            flash('The tag name has exsited', 'err')
            return redirect(url_for('admin.tag_add'))

        tag = Tag(
            name = data['name'],
            zodiac = ','.join(map(lambda v: str(v),data['zodiac']))
        )    
        db.session.add(tag)
        db.session.commit()
        flash('Add tag successfully', 'ok')
        oplog = Oplog(
            admin_id = session['admin_id'],
            ip = request.remote_addr,
            reason = 'Add tag:' + data['name']
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.tag_add'))
    return render_template('admin/tag_add.html', form=form)


@admin.route('/tag/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def tag_list(page=None):
    if page == None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.addtime.desc()
    ).paginate(page=page, per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('admin/tag_list.html',page_data = page_data, pages_num = pages_num)

@admin.route('/tag/del/<int:id>/', methods=['GET'])
@admin_login_req
@admin_auth
def tag_del(id=None):
    tag = Tag.query.filter_by(id = id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash('Delete tag sucessfully', 'ok')

    oplog = Oplog(
        admin_id = session['admin_id'],
        ip = request.remote_addr,
        reason = 'Delete tag:' + tag.name
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.tag_list', page=1))

@admin.route('/tag/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def tag_edit(id=None):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if request.method == 'GET':
        if tag.zodiac == '' or tag.zodiac == None:  
            form.zodiac.data = ''
        else:
            form.zodiac.data = list(map(lambda v: int(v), tag.zodiac.split(','))) 
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data['name']).count()
        if tag.name != data['name'] and tag_count == 1:
            flash('The tag name has existed!', 'err')
            return redirect(url_for('admin.tag_edit', id=id))
        tag.name = data['name']
        tag.zodiac = ','.join(map(lambda v: str(v),data['zodiac']))
        print('-------------')
        print(data['zodiac'])
        print(tag.zodiac)
        db.session.add(tag)
        db.session.commit()
        flash('Edit tag successfully','ok')
        return redirect(url_for('admin.tag_edit',id=id))
    return render_template('admin/tag_edit.html', form=form, tag=tag)  

@admin.route('/movie/add/', methods=['GET','POST'])
@admin_login_req
@admin_auth
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        movie = Movie.query.filter_by(title=data['title']).count()
        if movie == 1:
            flash('This movie has existed', 'err')
            return redirect(url_for('admin.movie_add'))
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)  
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], stat.S_IRWXU)
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config['UP_DIR'] + url)
        form.logo.data.save(app.config['UP_DIR'] + logo)
        movie = Movie(
            title = data['title'],
            url = url,
            info = data['info'],
            logo = logo,
            star = int(data['star']),
            playnum=0,
            commentnum=0,
            tags = ','.join(map(lambda v: str(v),data['tags'])),
            area = data['area'],
            release_time = data['release_time'],
            length = data['length']
        )
        db.session.add(movie)
        db.session.commit()
        flash('Add new movie successfully','ok')

        oplog = Oplog(
            admin_id = session['admin_id'],
            ip = request.remote_addr,
            reason = 'Add the movie: ' + movie.title 
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.movie_add'))
    return render_template('admin/movie_add.html', form=form)


@admin.route('/movie/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def movie_list(page=None):
    if page == None:
        page = 1
    page_data = Movie.query.order_by(
        Movie.addtime.desc()
    
    #)
    #page_data = Movie.query.join(Tag).filter(
    #    Tag.id == Movie.tag_id
    #).order_by(
 
    ).paginate(page=page, per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('admin/movie_list.html', page_data = page_data, pages_num = pages_num)


@admin.route('/movie/del/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def movie_del(id=None):
    movie = Movie.query.filter_by(id=id).first_or_404()
    db.session.delete(movie)
    db.session.commit()
    flash('Delete movie successfully','ok')

    oplog = Oplog(
        admin_id = session['admin_id'],
        ip = request.remote_addr,
        reason = 'Delete movie: '+ movie.title 
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.movie_list', page=1))

#Edit movie
@admin.route('/movie/edit/<int:id>/', methods=['GET','POST'])
@admin_login_req
@admin_auth
def movie_edit(id=None):
    form = MovieForm()
    form.url.validators = []
    form.logo.validators = []
    movie = Movie.query.get_or_404(id)
    if request.method == 'GET':
        if movie.tags == '':
            form.info.data = movie.info
            form.tags.data = movie.tags
            form.star.data = movie.star
        else:
            form.info.data = movie.info
            form.tags.data = list(map(lambda v: int(v), movie.tags.split(',')))
            form.star.data = movie.star   

    if form.validate_on_submit():
        data = form.data
        movie_count = Movie.query.filter_by(title=data['title']).count()
        if movie_count == 1 and movie.title != data['title']:
            flash('This name has existed, please input again', 'err')
            return redirect(url_for('admin.movie_edit',id=id))

        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'],stat.S_IRWXU)

        if form.url.data.filename != '':
            file_url = secure_filename(form.url.data.filename)
            movie.url = change_filename(file_url)
            form.url.data.save(app.config['UP_DIR'] + movie.url)

        if form.logo.data.filename != '':
            file_logo = secure_filename(form.logo.data.filename)
            movie.logo = change_filename(file_logo)
            form.logo.data.save(app.config['UP_DIR'] + movie.logo)

        movie.info = data['info']
        movie.star = data['star']
        movie.tags = ','.join(map(lambda v: str(v), data['tags']))
        movie.title = data['title']
        movie.area = data['area']
        movie.length = data['length']
        movie.release_time = data['release_time']
        db.session.add(movie)
        db.session.commit()

        flash('Edit movie successfully','ok')
        return redirect(url_for('admin.movie_edit', id=movie.id))
    return render_template('admin/movie_edit.html', form=form, movie=movie)



@admin.route('/music/add/', methods=['GET','POST'])
@admin_login_req
@admin_auth
def music_add():
    form = MusicForm()
    if form.validate_on_submit():
        data = form.data
        music = Music.query.filter_by(title=data['title']).count()
        if music == 1:
            flash('This music has existed', 'err')
            return redirect(url_for('admin.music_add'))
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)  
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], stat.S_IRWXU)
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config['UP_DIR'] + url)
        form.logo.data.save(app.config['UP_DIR'] + logo)
        music = Music(
            title = data['title'],
            url = url,
            info = data['info'],
            logo = logo,
            star = int(data['star']),
            playnum = 0,
            commentnum = 0,
            tags = ','.join(map(lambda v: str(v),data['tags'])),
            singer = data['singer'],
            release_time = data['release_time'],
            length = data['length']
        )
        db.session.add(music)
        db.session.commit()
        flash('Add new music successfully','ok')

        oplog = Oplog(
            admin_id = session['admin_id'],
            ip = request.remote_addr,
            reason = 'Add the music: ' + music.title
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.music_add'))

    return render_template('admin/music_add.html', form=form)


@admin.route('/music/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def music_list(page=None):
    if page == None:
        page = 1
    page_data = Music.query.order_by(
        Music.addtime.desc()
    ).paginate(page=page, per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('admin/music_list.html', page_data = page_data, pages_num = pages_num)


@admin.route('/music/del/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def music_del(id=None):
    music = Music.query.filter_by(id=id).first_or_404()
    db.session.delete(music)
    db.session.commit()
    flash('Delete music successfully','ok')

    oplog = Oplog(
        admin_id = session['admin_id'],
        ip = request.remote_addr,
        reason = 'Delete music: ' + music.title
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.music_list', page=1))

#Edit music
@admin.route('/music/edit/<int:id>/', methods=['GET','POST'])
@admin_login_req
@admin_auth
def music_edit(id=None):
    form = MusicForm()
    form.url.validators = []
    form.logo.validators = []
    music = Music.query.get_or_404(id)
    if request.method == 'GET':
        if music.tags == '':
            form.info.data = music.info
            form.tags.data = music.tags
            form.star.data = music.star
        else:    
            form.info.data = music.info
            form.tags.data = list(map(lambda v: int(v), music.tags.split(',')))
            form.star.data = music.star
        
    if form.validate_on_submit():
        data = form.data
        music_count = Music.query.filter_by(title=data['title']).count()
        if music_count == 1 and music.title != data['title']:
            flash('This name has existed, please input again', 'err')
            return redirect(url_for('admin.music_edit',id=id))

        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'],stat.S_IRWXU)

        if form.url.data.filename != '':
            file_url = secure_filename(form.url.data.filename)
            music.url = change_filename(file_url)
            form.url.data.save(app.config['UP_DIR'] + music.url)

        if form.logo.data.filename != '':
            file_logo = secure_filename(form.logo.data.filename)
            music.logo = change_filename(file_logo)
            form.logo.data.save(app.config['UP_DIR'] + music.logo)

        music.url = data['url']
        music.info = data['info']
        music.star = data['star']
        music.tags = ','.join(map(lambda v: str(v), data['tags']))
        music.title = data['title']
        music.singer = data['singer']
        music.length = data['length']
        music.release_time = data['release_time']
        db.session.add(music)
        db.session.commit()

        flash('Edit music successfully','ok')
        return redirect(url_for('admin.music_edit', id=music.id))
    return render_template('admin/music_edit.html', form=form, music=music)



@admin.route('/book/add/', methods=['GET','POST'])
@admin_login_req
@admin_auth
def book_add():
    form = BookForm()
    if form.validate_on_submit():
        data = form.data
        book = Book.query.filter_by(title=data['title']).count()
        if book == 1:
            flash('This book has existed', 'err')
            return redirect(url_for('admin.book_add'))
        file_logo = secure_filename(form.logo.data.filename)  
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], stat.S_IRWXU)
        logo = change_filename(file_logo)
        form.logo.data.save(app.config['UP_DIR'] + logo)
        book = Book(
            title = data['title'],
            url = data['url'],
            info = data['info'],
            logo = logo,
            star = int(data['star']),
            commentnum=0,
            tags = ','.join(map(lambda v: str(v),data['tags'])),
            author = data['author'],
            release_time = data['release_time']
        )
        db.session.add(book)
        db.session.commit()
        flash('Add new book successfully','ok')

        oplog = Oplog(
            admin_id = session['admin_id'],
            ip = request.remote_addr,
            reason = 'Add the book: ' + book.title
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.book_add'))

    return render_template('admin/book_add.html', form=form)


@admin.route('/book/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def book_list(page=None):
    if page == None:
        page = 1
    page_data = Book.query.order_by(
        Book.addtime.desc()
    ).paginate(page=page, per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('admin/book_list.html', page_data = page_data, pages_num = pages_num)


@admin.route('/book/del/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def book_del(id=None):
    book = Book.query.filter_by(id=id).first_or_404()
    db.session.delete(book)
    db.session.commit()
    flash('Delete book successfully','ok')

    oplog = Oplog(
        admin_id = session['admin_id'],
        ip = request.remote_addr,
        reason = 'Delete book: ' + book.title
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.book_list', page=1))

#Edit book
@admin.route('/book/edit/<int:id>/', methods=['GET','POST'])
@admin_login_req
@admin_auth
def book_edit(id=None):
    form = BookForm()
    form.url.validators = []
    form.logo.validators = []
    book = Book.query.get_or_404(id)
    if request.method == 'GET':
        if book.tags == '':
            form.info.data = book.info
            form.tags.data = book.tags
            form.star.data = book.star
        else:
            form.info.data = book.info
            form.tags.data = list(map(lambda v: int(v), book.tags.split(',')))
            form.star.data = book.star    

    if form.validate_on_submit():
        data = form.data
        book_count = Book.query.filter_by(title=data['title']).count()
        if book_count == 1 and book.title != data['title']:
            flash('This name has existed, please input again', 'err')
            return redirect(url_for('admin.book_edit',id=id))

        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'],stat.S_IRWXU)

        if form.logo.data.filename != '':
            file_logo = secure_filename(form.logo.data.filename)
            book.logo = change_filename(file_logo)
            form.logo.data.save(app.config['UP_DIR'] + book.logo)

        book.info = data['info']
        book.star = data['star']
        book.tags = ','.join(map(lambda v: str(v), data['tags']))
        book.title = data['title']
        book.author = data['author']
        book.url = data['url']
        book.release_time = data['release_time']
        db.session.add(book)
        db.session.commit()

        flash('Edit book successfully','ok')
        return redirect(url_for('admin.book_edit', id=book.id))
    return render_template('admin/book_edit.html', form=form, book=book)




@admin.route('/preview/add/', methods=['GET','POST'])
@admin_login_req
@admin_auth
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        preview_count = Preview.query.filter_by(title=data['title']).count()
        if preview_count == 1:
            flash('The preview has exsited','err')
            return redirect(url_for('admin.preview_add'))            
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], stat.S_IRWXU)
        logo = change_filename(file_logo)
        form.logo.data.save(app.config['UP_DIR'] + logo)
        preview = Preview(
            title = data['title'],
            logo = logo
        )
        db.session.add(preview)
        db.session.commit()
        flash('Add the new preview successfully','ok')

        oplog = Oplog(
            admin_id = session['admin_id'],
            ip = request.remote_addr,
            reason = 'Add the preview:' + preview.title
        )

        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.preview_add'))
    return render_template('admin/preview_add.html', form=form)

@admin.route('/preview/list/<int:page>/', methods=['GET','POST'])
@admin_login_req
@admin_auth
def preview_list(page=None):
    if page == None:
        page = 1
    page_data = Preview.query.order_by(
        Preview.addtime.desc()
    ).paginate(page=page, per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('admin/preview_list.html', page_data=page_data, pages_num = pages_num)

@admin.route('/preview/del/<int:id>/', methods=['GET','POST'])
@admin_login_req
@admin_auth
def preview_del(id=None):
    preview = Preview.query.filter_by(id=id).first_or_404()
    db.session.delete(preview)
    db.session.commit()
    flash('Delete preview successfully','ok')   

    oplog = Oplog(
        admin_id = session['admin_id'],
        ip = request.remote_addr,
        reason = 'Delete the preview:' + preview.title
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.preview_list', page=1))

@admin.route('/preview/edit/<int:id>/', methods=['GET','POST'])
@admin_login_req
@admin_auth
def preview_edit(id=None):
    form = PreviewForm()
    form.logo.validators = []
    preview = Preview.query.get_or_404(id)
    if request.method == 'GET':
        form.title.data = preview.title
        form.logo.data = preview.logo
    if form.validate_on_submit():
        data = form.data
        preview_count = Preview.query.filter_by(title=data['title']).count()
        if preview_count == 1 and preview.title != data['title']:
            flash('The preview has exisited, please input again','err')
            return redirect(url_for('admin.preview_edit',id=id))

        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'],stat.S_IRWXU)

        if form.logo.data != '':             
            file_logo = secure_filename(form.logo.data.filename)
            preview.logo = change_filename(file_logo)
            form.logo.data.save(app.config['UP_DIR'] + preview.logo)

        preview.title = data['title']
        db.session.add(preview)
        db.session.commit()
        flash('Modify preview successfully','ok')
        return redirect(url_for('admin.preview_edit', id=preview.id))

    return render_template('admin/preview_edit.html', form=form, preview=preview)

@admin.route('/user/list/<int:page>/', methods=['GET','POST'])
@admin_login_req
@admin_auth
def user_list(page=None):
    if page == None:
        page = 1
    page_data = User.query.order_by(
        User.addtime.desc()
    ).paginate(page=page, per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('admin/user_list.html', page_data=page_data, pages_num = pages_num)

@admin.route('/user/view/<int:id>/', methods=['GET','POST'])
@admin_login_req
@admin_auth
def user_view(id=None):
    user = User.query.get_or_404(id)
    return render_template('admin/user_view.html', user=user)

@admin.route('/user/del/<int:id>/',methods=['GET','POST'])
@admin_login_req
@admin_auth
def user_del(id = None):
    user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    flash('Delete user successfully','ok')

    oplog = Oplog(
        admin_id = session['admin_id'],
        ip = request.remote_addr,
        reason = 'Delete the user:' + user.name
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.user_list', page=1))

@admin.route('/comment/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def comment_list(page=None):
    if page == None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Comment.movie_id,
        User.id == Comment.user_id
    ).order_by(
        Comment.addtime.desc()
    ).union(
        Comment.query.join(
            Music
        ).join(
            User
        ).filter(
            Music.id == Comment.music_id,
            User.id == Comment.user_id
        ).order_by(
            Comment.addtime.desc()
        ) 
    ).union(
        Comment.query.join(
            Book
        ).join(
            User
        ).filter(
            Book.id == Comment.book_id,
            User.id == Comment.user_id
        ).order_by(
            Comment.addtime.desc()
        ) 
    ).paginate(page=page, per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('admin/comment_list.html', page_data=page_data, pages_num = pages_num)

@admin.route('/comment/del/<int:id>/', methods=['GET'])
@admin_login_req
@admin_auth
def comment_del(id=None):
    comment = Comment.query.filter_by(id = id).first_or_404()
    db.session.delete(comment)
    db.session.commit()
    flash('Delete comment successfully','ok')

    oplog = Oplog(
        admin_id = session['admin_id'],
        ip = request.remote_addr,
        reason = 'Delete the comment:' + comment.content
    )
    db.session.add(oplog)
    de.session.commit()
    return redirect(url_for('admin.comment_list',page=1))


@admin.route('/moviecol/list/<int:page>/',methods=['GET'])
@admin_login_req
@admin_auth
def moviecol_list(page=None):
    if page == None:
        page = 1
    page_data = Moviecol.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Moviecol.movie_id,
        User.id == Moviecol.user_id
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page, per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('admin/moviecol_list.html',page_data=page_data, pages_num = pages_num)

@admin.route('/moviecol/del/<int:id>/', methods=['GET'])
@admin_login_req
@admin_auth
def moviecol_del(id=None):
    moviecol = Moviecol.query.filter_by(id=id).first_or_404()
    db.session.delete(moviecol)
    db.session.commit()
    flash('Delete movie collection successfully','ok')
    return redirect(url_for('admin.moviecol_list',page=1))


@admin.route('/musiccol/list/<int:page>/',methods=['GET'])
@admin_login_req
@admin_auth
def musiccol_list(page=None):
    if page == None:
        page = 1
    page_data = Musiccol.query.join(
        Music
    ).join(
        User
    ).filter(
        Music.id == Musiccol.music_id,
        User.id == Musiccol.user_id
    ).order_by(
        Musiccol.addtime.desc()
    ).paginate(page=page, per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('admin/musiccol_list.html',page_data=page_data, pages_num = pages_num)

@admin.route('/musiccol/del/<int:id>/', methods=['GET'])
@admin_login_req
@admin_auth
def musiccol_del(id=None):
    musiccol = Musiccol.query.filter_by(id=id).first_or_404()
    db.session.delete(musiccol)
    db.session.commit()
    flash('Delete music collection successfully','ok')
    return redirect(url_for('admin.musiccol_list',page=1))

@admin.route('/bookcol/list/<int:page>/',methods=['GET'])
@admin_login_req
@admin_auth
def bookcol_list(page=None):
    if page == None:
        page = 1
    page_data = Bookcol.query.join(
        Book
    ).join(
        User
    ).filter(
        Book.id == Bookcol.book_id,
        User.id == Bookcol.user_id
    ).order_by(
        Bookcol.addtime.desc()
    ).paginate(page=page, per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('admin/bookcol_list.html',page_data=page_data, pages_num = pages_num)

@admin.route('/bookcol/del/<int:id>/', methods=['GET'])
@admin_login_req
@admin_auth
def bookcol_del(id=None):
    bookcol = Bookcol.query.filter_by(id=id).first_or_404()
    db.session.delete(bookcol)
    db.session.commit()
    flash('Delete book collection successfully','ok')
    return redirect(url_for('admin.bookcol_list',page=1))    


@admin.route('/oplog/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def oplog_list(page=None):
    if page == None:
        page = 1
    page_data = Oplog.query.join(
        Admin
    ).filter(
        Admin.id == Oplog.admin_id
    ).order_by(
        Oplog.addtime.desc()
    ).paginate(page=page, per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('admin/oplog_list.html', page_data=page_data, pages_num = pages_num)

@admin.route('/adminloginlog/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def adminloginlog_list(page=None):
    if page == None:
        page = 1
    page_data = Adminlog.query.join(
        Admin
    ).filter(
        Admin.id == Adminlog.admin_id
    ).order_by(
        Adminlog.addtime.desc()
    ).paginate(page=page, per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('admin/adminloginlog_list.html', page_data=page_data, pages_num = pages_num)

@admin.route('/userloginlog/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def userloginlog_list(page=None):
    if page == None:
        page = 1
    page_data = Userlog.query.join(
        User
    ).filter(
        User.id == Userlog.user_id
    ).order_by(
        Userlog.addtime.desc()
    ).paginate(page=page, per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('admin/userloginlog_list.html', page_data = page_data, pages_num = pages_num)

@admin.route('/auth/add/', methods=['GET','POST'])
@admin_login_req
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth_count = Auth.query.filter_by(name=data['name']).count()
        if auth_count == 1:
            flash('The authority name has existed, please add again','err')
            return redirect(url_for('admin.auth_add'))
        auth = Auth(
            name = data['name'],
            url = data['url']
        )
        db.session.add(auth)
        db.session.commit() 
        flash('Add the new authority successfully','ok')
        return redirect(url_for('admin.auth_add'))
    return render_template('admin/auth_add.html', form=form)

@admin.route('/auth/list/<int:page>/', methods=['GET'])
@admin_login_req
def auth_list(page=None):
    if page == None:
        page = 1
    page_data = Auth.query.order_by(
        Auth.addtime.desc()
    ).paginate(page=page, per_page = 10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('admin/auth_list.html', page_data=page_data, pages_num = pages_num)

@admin.route('/auth/del/<int:id>/', methods=['GET'])
@admin_login_req
@admin_auth
def auth_del(id = None):
    auth = Auth.query.filter_by(id=id).first_or_404()
    db.session.delete(auth)
    db.session.commit()
    flash('Delete authority successfully','ok')
    return redirect(url_for('admin.auth_list', page=1))   

@admin.route('/auth/edit/<int:id>/', methods=['GET','POST'])
@admin_login_req
def auth_edit(id=None):
    form = AuthForm()
    auth = Auth.query.get_or_404(id)
    if request.method == 'GET':
        form.name.data = auth.name
        form.url.data = auth.url
    if form.validate_on_submit():
        data = form.data
        auth_count = Auth.query.filter_by(name=data['name']).count()
        if auth_count == 1 and auth.name != data['name']:
            flash('The authority name has existed, please input again','err')
            return redirect(url_for('admin.auth_edit', id=id))
        auth.name = data['name']
        auth.url = data['url']
        db.session.add(auth)
        db.session.commit()
        flash('Modify authority successfully','ok')
        return redirect(url_for('admin.auth_edit', id=auth.id))

    return render_template('admin/auth_edit.html', form=form)


@admin.route('/role/add/', methods=['GET', 'POST'])
@admin_login_req
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        role_count = Role.query.filter_by(name=data['name']).count()
        if role_count == 1:
            flash('The role name has existed, please add again', 'err')
            return redirect(url_for('admin.role_add'))
        role = Role(
            name = data['name'],
            auths = ','.join(map(lambda v: str(v),data['auths']))
        )
        db.session.add(role)
        db.session.commit()
        flash('Add new role successfully','ok')
        return redirect(url_for('admin.role_add'))
    return render_template('admin/role_add.html', form=form)


@admin.route('/role/list/<int:page>/', methods=['GET'])
@admin_login_req
def role_list(page=None):
    if page == None:
        page = 1
    page_data = Role.query.order_by(
        Role.addtime.desc()
    ).paginate(page=page, per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('admin/role_list.html', page_data=page_data, pages_num = pages_num)


@admin.route('/role/del/<int:id>/', methods=['GET'])
@admin_login_req
@admin_auth
def role_del(id=None):
    role = Role.query.filter_by(id=id).first_or_404()
    db.session.delete(role)
    db.session.commit()
    flash('Delete role successfully', 'ok')
    return redirect(url_for('admin.role_list', page=1))


@admin.route('/role/edit/<int:id>/', methods=['GET','POST'])
@admin_login_req
def role_edit(id=None):
    form = RoleForm()
    role = Role.query.get_or_404(id)
    if request.method == 'GET':
        if role.auths == '':
            form.name.data = role.name
        else:
            form.name.data = role.name
            form.auths.data = list(map(lambda v: int(v), role.auths.split(',')))  

    if form.validate_on_submit():
        data = form.data
        role_count = Role.query.filter_by(name=data['name']).count()
        if role_count == 1 and role.name != data['name']:
            flash('The role name has existed, please input again', 'err')
            return redirect(url_for('admin.role_edit', id=id))
        role.name = data['name']
        role.auths = ','.join(map(lambda v: str(v), data['auths']))
        db.session.add(role)
        db.session.commit()
        flash('Modify role successfully', 'ok')
        return redirect(url_for('admin.role_edit', id=role.id))

    return render_template('admin/role_edit.html', form=form)

@admin.route('/admin/add/',methods=['GET','POST'])
@admin_login_req
@admin_auth
def admin_add():
    form = AdminForm()
    from werkzeug.security import generate_password_hash
    if form.validate_on_submit():
        data = form.data
        admin_count = Admin.query.filter_by(name=data['name']).count()
        if admin_count == 1:
            flash('This admin has existed, please add again','err')
            return redirect(url_for('admin.admin_add'))
        admin = Admin(
            name = data['name'],
            pwd = generate_password_hash(data['pwd']),
            role_id = data['role_id'],
            is_super = 1
        )
        db.session.add(admin)
        db.session.commit()
        flash('Add new admin successfully','ok')
        return redirect(url_for('admin.admin_add'))
    return render_template('admin/admin_add.html', form=form)

    
@admin.route('/admin/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def admin_list(page=None):
    if page == None:
        page = 1
    page_data = Admin.query.join(
        Role
    ).filter(
        Role.id == Admin.role_id
    ).order_by(
        Admin.addtime.desc()
    ).paginate(page=page, per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('admin/admin_list.html',page_data=page_data, pages_num = pages_num)


















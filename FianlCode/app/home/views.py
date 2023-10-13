#!/user/bin/env python
#-*- coding:utf-8 -*-
#time: 2019/6/7
__author__ = 'Wei'

from . import home
from flask import render_template, url_for, redirect, flash, session, request
from app.home.forms import RegistForm, LoginForm, UserdetailForm, PwdForm, CommentForm
from app.models import User, Userlog, Comment, Movie, Preview, Tag, Moviecol, Know, Music, Book, Musiccol, Bookcol
from app import db, app
import uuid
from werkzeug.security import generate_password_hash
from functools import wraps
from werkzeug.utils import secure_filename
import os, stat, datetime
from sqlalchemy import and_,or_,not_
from datetime import date
import math

def change_filename(filename):
    fileinfo = filename.split('.')
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + '.' + fileinfo[-1]
    return filename


def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('home.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@home.route('/', methods=['GET'])
def index_1():
    return redirect('/1/')

@home.route('/<int:page>/', methods=['GET'])
def index(page=None):
    tags = Tag.query.all()
    page_data = Movie.query.order_by(
        Movie.addtime.desc()
    )
    tid = request.args.get('tid',0)
    if int(tid) != 0:
        page_data = page_data.filter_by(tag_id = int(tid))
    
    star = request.args.get('star',0)
    if int(star) != 0:
        page_data = page_data.filter_by(star=int(star))

    time = request.args.get('time', 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = Movie.query.order_by(
                Movie.addtime.desc()
            )
        else:
            page_data = Movie.query.order_by(
                Movie.addtime.asc()
            )

    pm = request.args.get('pm',0)
    if int(pm) != 0:
        if int(pm) == 1:
            page_data = Movie.query.order_by(
                Movie.playnum.desc()
            )        
        else:
            page_data = Movie.query.order_by(
                Movie.playnum.asc()
            )

    cm = request.args.get('cm',0)
    if int(cm) != 0:
        if int(cm) == 1:
            page_data = Movie.query.order_by(
                Movie.commentnum.desc()
            )
        else:
            page_data = Movie.query.order_by(
                Movie.commentnum.asc()
            )      

    if page == None:
        page = 1
    page_data = page_data.paginate(page=page, per_page=10)

    p = dict(
        tid = tid,
        star = star,
        time = time,
        pm = pm,
        cm = cm
    )
    pages_num = math.ceil(page_data.total/10)
    return render_template('home/index.html', tags=tags, p=p, page_data=page_data, pages_num = pages_num)

#login
@home.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['name']).first()
        if not user:
            flash('The username does not exist', 'err')
            return redirect(url_for('home.login'))
        if user.check_pwd(data['pwd']) == False:
            flash('The password is wrong','err')
            return redirect(url_for('home.login'))
        session['user'] = user.name
        session['user_id'] = user.id

        userlog = Userlog(
            user_id = session['user_id'],
            ip = request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return render_template('home/index.html', form=form, user=user)
    return render_template('home/login.html', form=form)

@home.route('/logout/')
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('home.login'))

@home.route('/regist/', methods=['GET','POST'])
def regist():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        name = data['name']
        user = User.query.filter_by(name=name).count()
        if user == 1:
            flash('This username has existed','err')
            return render_template('home/regist.html', form=form)

        email = data['email']
        user = User.query.filter_by(email=email).count()
        if user == 1:
            flash('This email has existed', 'err')
            return render_template('home/regist.html', form=form)

        phone = data['phone']
        user = User.query.filter_by(phone=phone).count()
        if user == 1:
            flash('This phone no. has existed', 'err')
            return render_template('home/regist.html', form=form)

        user = User(
            name = data['name'],
            email = data['email'],
            phone = data['phone'],
            pwd = generate_password_hash(data['pwd']),
            uuid = uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash('congratulations, register successful!','ok')
        return redirect(url_for('home.login'))
    return render_template('home/regist.html', form = form)        

@home.route('/user/', methods=['GET','POST'])
@user_login_req
def user():
    form = UserdetailForm()
    user = User.query.get_or_404(session['user_id'])
    form.face.validators = []
    if request.method == 'GET':
        form.name.data = user.name
        form.dob.data = user.DOB
        form.gender.data = user.gender
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
        form.facebook.data = user.facebook
        form.instagram.data = user.instagram
        form.twitter.data = user.twitter

    if form.validate_on_submit():
        data = form.data 
        user_count = User.query.filter_by(name = data['name']).count()
        if user_count == 1 and user.name != data['name']:
            flash('The user has existed, please input again','err')
            return redirect(url_for('home.user'))

        user_email = User.query.filter_by(email=data['email']).count()
        if user_email == 1 and user.email != data['email']:
            flash('The email has existed, please input again', 'err')
            return redirect(url_for('home.user'))

        user_phone = User.query.filter_by(email=data['phone']).count()
        if user_phone == 1 and user.phone != data['phone']:
            flash('The phone no has existed, please input again', 'err')
            return redirect(url_for('home.user'))

        if not os.path.exists(app.config['FC_DIR']):
            os.mkdir(app.config['FC_DIR'])
            os.chmod(app.config['FC_DIR'], stat.S_IRWXU)

        if form.face.data.filename != '':
            file_face = secure_filename(form.face.data.filename)
            user.face = change_filename(file_face)
            form.face.data.save(app.config['FC_DIR'] + user.face)
        


        user.name = data['name'],
        user.DOB = data['dob'],
        user.gender = data['gender'],
        user.email = data['email'],
        user.phone = data['phone'],
        user.facebook = data['facebook'],
        user.instagram = data['instagram'],
        user.twitter = data['twitter'],
        user.info = data['info'],

        db.session.add(user)
        db.session.commit()

        
        know =  Know.query.filter_by(user_id = user.id).first()
       # know_count = Know.query.filter_by(user_id = user.id).count()
        if know == None :
            year = user.DOB.year
            month = user.DOB.month
            date = user.DOB.day
            zodiac_cz = ChineseZodiac(year)
            zodiac_z = Zodiac(month,date)
            know = Know(
                user_id = user.id,
                strengths = zodiac_cz[1] + zodiac_z[1],
                weaknesses = zodiac_cz[2] + zodiac_z[2],
                jobs = zodiac_cz[3],
                luckNum = zodiac_cz[4],
                luckColor = zodiac_cz[5],
                luckFlower = zodiac_cz[6], 
                luckDirection = zodiac_cz[7],
                likes = zodiac_z[3],
                dislikes = zodiac_z[4],
                zodiac_info = zodiac_z[0],
                chineseZodiac_info = zodiac_cz[0],
                zodiac = zodiac_z[5],
                chineseZodiac = zodiac_cz[8],
            )
            db.session.add(know)
            db.session.commit()
            flash('You have update your detailed info, you can check your report!','ok')
            return redirect(url_for('home.know'))            
        flash('Modify info successfully!','ok')
        return redirect(url_for('home.user'))    
    return render_template('home/user.html', form=form, user=user)

@home.route('/pwd/', methods=['GET','POST'])
@user_login_req
def pwd():
    form = PwdForm()
    user = User.query.filter_by(id=session['user_id']).first()
    if form.validate_on_submit():
        data = form.data
        if not user.check_pwd(data['old_pwd']):
            flash('The old password is wrong, please input again','err')
            return redirect(url_for('home.pwd'))
        user.pwd = generate_password_hash(data['new_pwd'])
        db.session.add(user)
        db.session.commit()
        flash('Modify the password successfully','ok')
        return redirect(url_for('home.logout'))
    return render_template('home/pwd.html', form=form)
    

@home.route('/know/', methods=['GET','POST'])
@user_login_req
def know(page=None):
    user = User.query.get_or_404(session['user_id'])
    match = {"Capricorn":["Scorpio","Pisces"],"Aquarius":["Aries","Sagittarius"],"Pisces":["Aries","Taurus"],"Aries":["Aquarius","Gemini"],"Taurus":["Pisces","Cancer"],"Gemini":["Aries","Leo"],"Cancer":["Taurus","Virgo"],"Leo":["Gemini","Libra"],"Virgo":["Cancer","Scorpio"],"Libra":["Leo","Sagittarius"],"Scorpio":["Virgo","Aries"],"Sagittarius":["Libra","Aquarius"]}
    record_count = Know.query.filter_by(user_id=session['user_id']).count()
    record = Know.query.filter_by(user_id=session['user_id']).first()
    if record_count == 1:
        if page == None:
            page = 1 
        page_data= db.session.query(User.name, User.face, User.DOB, User.info, User.facebook, User.twitter, User.instagram, Know.zodiac, Know.chineseZodiac).join(
            Know, User.id == Know.user_id 
        ).filter(
            User.id != session['user_id']
        ).paginate(page = page, per_page = 3)  

        for u in page_data.items:
            if abs(date(user.DOB.year, user.DOB.month, user.DOB.day) - date(u.DOB.year, u.DOB.month, u.DOB.day)) > datetime.timedelta(days=1095):
                page_data.items.remove(u)
            elif u.zodiac not in match[record.zodiac]:
                page_data.items.remove(u)
        pages_num = math.ceil(page_data.total/10)
        return render_template('home/know.html', user=user, record=record, page_data=page_data, match=match, pages_num = pages_num)
    else:
        flash('If you want to check report, please input your birthday', 'info')
        return redirect(url_for('home.user'))

@home.route('/comments/<int:page>', methods=['GET'])
@user_login_req
def comments(page=None):
    if page == None:
        page = 1
        
    page_data = Comment.query.join(
        User
    ).join(
        Movie
    ).filter(
        Comment.user_id == session['user_id'],
        User.id == Comment.user_id,
        Movie.id == Comment.movie_id
    ).order_by(
        Comment.addtime.desc()
    ).union(
        Comment.query.join(
            User
        ).join(
            Music
        ).filter(
            Comment.user_id == session['user_id'],
            User.id == Comment.user_id,
            Music.id == Comment.music_id
        ).order_by(
            Comment.addtime.desc()
        )
    ).union(
        Comment.query.join(
            User
        ).join(
            Book
        ).filter(
            Comment.user_id == session['user_id'],
            User.id == Comment.user_id,
            Book.id == Comment.book_id
        ).order_by(
            Comment.addtime.desc()
        )
    ).paginate(page=page, per_page=6)  
    pages_num = math.ceil(page_data.total/10)
    return render_template('home/comments.html', page_data=page_data, pages_num = pages_num)

#login log
@home.route('/loginlog/<int:page>/', methods=['GET'])
@user_login_req
def loginlog(page=None):
    if page == None:
        page = 1
    page_data = Userlog.query.filter_by(
        user_id = session['user_id']
    ).order_by(
        Userlog.addtime.desc()
    ).paginate(page=page, per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('home/loginlog.html', page_data=page_data, pages_num = pages_num)

@home.route('/moviecol/<int:page>/', methods=['GET'])
@user_login_req
def moviecol(page=None):
    if page == None:
        page = 1
    page_data = Moviecol.query.join(
        Movie
    ).filter(
        Moviecol.user_id == session['user_id']
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page,per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('home/moviecol.html', page_data = page_data, pages_num = pages_num)

@home.route('/moviecol/add/', methods=['GET'])
@user_login_req
def moviecol_add():
    uid = request.args.get("uid","")
    mid = request.args.get("mid","")
    moviecol = Moviecol.query.filter_by(
        # user_id = int(uid),
        # movie_id = int(mid)
        movie_id = mid,
        user_id = uid
    ).count()
    if moviecol == 1:
        data = dict(ok=0)
    else:
        moviecol = Moviecol(
            movie_id = mid,
            user_id = uid
        )
        db.session.add(moviecol)
        db.session.commit()
        data = dict(ok=1)
    import  json
    return json.dumps(data)


@home.route('/musiccol/<int:page>/', methods=['GET'])
@user_login_req
def musiccol(page=None):
    if page == None:
        page = 1
    page_data = Musiccol.query.join(
        Music
    ).filter(
        Musiccol.user_id == session['user_id']
    ).order_by(
        Musiccol.addtime.desc()
    ).paginate(page=page,per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('home/musiccol.html', page_data = page_data, pages_num = pages_num)


@home.route('/musiccol/add/', methods=['GET'])
@user_login_req
def musiccol_add():
    uid = request.args.get("uid","")
    mid = request.args.get("mid","")
    musiccol = Musiccol.query.filter_by(
        # user_id = int(uid),
        # movie_id = int(mid)
        music_id = mid,
        user_id = uid
    ).count()
    if musiccol == 1:
        data = dict(ok=0)
    else:
        musiccol = Musiccol(
            music_id = mid,
            user_id = uid
        )
        db.session.add(musiccol)
        db.session.commit()
        data = dict(ok=1)

    import  json
    return json.dumps(data)


@home.route('/bookcol/<int:page>/', methods=['GET'])
@user_login_req
def bookcol(page=None):
    if page == None:
        page = 1
    page_data = Bookcol.query.join(
        Book
    ).filter(
        Bookcol.user_id == session['user_id']
    ).order_by(
        Bookcol.addtime.desc()
    ).paginate(page=page,per_page=10)
    pages_num = math.ceil(page_data.total/10)
    return render_template('home/bookcol.html', page_data = page_data, pages_num = pages_num)


@home.route('/bookcol/add/', methods=['GET'])
@user_login_req
def bookcol_add():
    uid = request.args.get("uid","")
    mid = request.args.get("mid","")
    bookcol = Bookcol.query.filter_by(
        # user_id = int(uid),
        # movie_id = int(mid)
        book_id = mid,
        user_id = uid
    ).count()
    if bookcol == 1:
        data = dict(ok=0)
    else:
        bookcol = Bookcol(
            book_id = mid,
            user_id = uid
        )
        db.session.add(bookcol)
        db.session.commit()
        data = dict(ok=1)

    import  json
    return json.dumps(data)


@home.route('/movierecommend/<int:page>/', methods=['GET'])
@user_login_req
def movierec(page=None):
    user = User.query.get_or_404(session['user_id'])
    record_count = Know.query.filter_by(user_id=session['user_id']).count()
    record = Know.query.filter_by(user_id=session['user_id']).first()
    tags = Tag.query.all()
    u_tags = []
    for t in tags:
        if record.zodiac in t.zodiac.split(','):
            u_tags.append(t.id)

    if page == None:
        page = 1
    page_data = Movie.query.filter(
        Movie.star >= 4
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page,per_page=10)

    for data in page_data.items:
        temp_tags = set(data.tags.split(','))
        list_common = list(temp_tags.intersection(set(u_tags)))
        if len(list_common) <3:
            page_data.items.remove(data)

    pages_num = math.ceil(page_data.total/10)
    return render_template('home/movie_recommend.html', page_data = page_data, user = user, record = record, pages_num = pages_num)   


@home.route('/musicrecommend/<int:page>/', methods=['GET'])
@user_login_req
def musicrec(page=None):
    user = User.query.get_or_404(session['user_id'])
    record_count = Know.query.filter_by(user_id=session['user_id']).count()
    record = Know.query.filter_by(user_id=session['user_id']).first()
    tags = Tag.query.all()
    u_tags = []
    for t in tags:
        if record.zodiac in t.zodiac.split(','):
            u_tags.append(t.id)

    if page == None:   
        page = 1
    page_data = Music.query.filter(
        Music.star == 5
    ).order_by(
        Music.addtime.desc()
    ).paginate(page=page,per_page=10)

    for data in page_data.items:
        temp_tags = set(data.tags.split(','))
        list_common = list(temp_tags.intersection(set(u_tags)))
        if len(list_common) <3:
            page_data.items.remove(data)

    pages_num = math.ceil(page_data.total/10)
    return render_template('home/music_recommend.html', page_data = page_data, user = user, record = record, pages_num = pages_num)  

@home.route('/bookrecommend/<int:page>/', methods=['GET'])
@user_login_req
def bookrec(page=None):
    user = User.query.get_or_404(session['user_id'])
    record_count = Know.query.filter_by(user_id=session['user_id']).count()
    record = Know.query.filter_by(user_id=session['user_id']).first()
    tags = Tag.query.all()
    u_tags = []
    for t in tags:
        if record.zodiac in t.zodiac.split(','):
            u_tags.append(t.id)
            
    if page == None:   
        page = 1
    page_data = Book.query.filter(
        Book.star == 5
    ).order_by(
        Book.addtime.desc()
    ).paginate(page=page,per_page=10)


    for data in page_data.items:
        temp_tags = set(data.tags.split(','))
        list_common = list(temp_tags.intersection(set(u_tags)))
        if len(list_common) <3:
            page_data.items.remove(data)

    pages_num = math.ceil(page_data.total/10)
    return render_template('home/book_recommend.html', page_data = page_data, user = user, record = record, pages_num = pages_num)  


@home.route('/animation/')
def animation():
    data = Preview.query.all()
    return render_template('home/animation.html',data=data)

@home.route('/search/<int:page>/')
def search(page=None):
    if page == None:
        page = 1
    key = request.args.get('key','')
    page_data = db.session.query(Movie.id, Movie.title, Movie.logo, Movie.info).filter(
        Movie.title.ilike('%' + key + '%')
    ).order_by(
        Movie.addtime.desc()
    ).union(
        db.session.query(Music.id, Music.title, Music.logo, Music.info).filter(
            Music.title.ilike('%' + key + '%')
        ).order_by(
            Music.addtime.desc()
        )
    ).union(
        db.session.query(Book.id, Book.title, Book.logo, Book.info).filter(
            Book.title.ilike('%' + key + '%')
        ).order_by(
            Book.addtime.desc()
        )
    ).paginate(page=page, per_page=10)

    movie_count = Movie.query.filter(
        Movie.title.ilike('%' + key + '%')
    ).count()
    music_count = Music.query.filter(
        Music.title.ilike('%' + key + '%')
    ).count()
    book_count = Book.query.filter(
        Book.title.ilike('%' + key + '%')
    ).count()
    total_count = movie_count + music_count + book_count
    page_data.key = key
    pages_num = math.ceil(page_data.total/10)
    return render_template('home/search.html', key=key, page_data=page_data, movie_count=movie_count, music_count=music_count, book_count=book_count, total_count=total_count, pages_num = pages_num)

@home.route('/play/<int:id>/<int:page>/', methods=['GET','POST'])
def play(id=None, page=None):
    form = CommentForm()
    movie = Movie.query.get_or_404(id)
    movie.playnum = movie.playnum + 1
    tags_id = list(map(lambda v: int(v), movie.tags.split(',')))
    tags = []
    for t in tags_id:
        temp_tag=Tag.query.filter_by(id=t).first()
        tags.append(temp_tag.name)
    if page == None:
        page = 1
    page_data = Comment.query.join(
        User
    ).filter(
        User.id == Comment.user_id,
        Comment.movie_id == id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page = page, per_page = 6)
    if 'user' in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content = data['content'],
            movie_id = id,
            user_id = session['user_id']
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment Successfully')
        
        movie.commentnum = movie.commentnum + 1
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('home.play',id=id,page=1))
        
    db.session.add(movie)
    db.session.commit()
    pages_num = math.ceil(page_data.total/10)
    return render_template('home/play.html', movie=movie, tags=tags, form=form, page_data=page_data, pages_num = pages_num)

@home.route('/play_music/<int:id>/<int:page>/', methods=['GET','POST'])
def playmusic(id=None, page=None):
    form = CommentForm()
    music = Music.query.get_or_404(id)
    music.playnum = music.playnum + 1
    tags_id = list(map(lambda v: int(v), music.tags.split(',')))
    tags = []
    for t in tags_id:
        temp_tag=Tag.query.filter_by(id=t).first()
        tags.append(temp_tag.name)
    if page == None:
        page = 1
    page_data = Comment.query.join(
        User
    ).filter(
        User.id == Comment.user_id,
        Comment.music_id == id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page = page, per_page = 6)
    if 'user' in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content = data['content'],
            music_id = id,
            user_id = session['user_id']
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment Successfully')
        
        music.commentnum = music.commentnum + 1
        db.session.add(music)
        db.session.commit()
        return redirect(url_for('home.playmusic',id=id,page=1))
        
    db.session.add(music)
    db.session.commit()
    pages_num = math.ceil(page_data.total/10)
    return render_template('home/play_music.html', music=music, tags=tags, form=form, page_data=page_data, pages_num = pages_num)    

@home.route('/play_book/<int:id>/<int:page>/', methods=['GET','POST'])
def playbook(id=None, page=None):
    form = CommentForm()
    book = Book.query.get_or_404(id)
    tags_id = list(map(lambda v: int(v), book.tags.split(',')))
    tags = []
    for t in tags_id:
        temp_tag=Tag.query.filter_by(id=t).first()
        tags.append(temp_tag.name)
    if page == None:
        page = 1
    page_data = Comment.query.join(
        User
    ).filter(
        User.id == Comment.user_id,
        Comment.book_id == id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page = page, per_page = 6)
    if 'user' in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content = data['content'],
            book_id = id,
            user_id = session['user_id']
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment Successfully')
        
        book.commentnum = book.commentnum + 1
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home.playbook',id=id,page=1))
        
    db.session.add(book)
    db.session.commit()
    pages_num = math.ceil(page_data.total/10)
    return render_template('home/play_book.html', book=book, tags=tags, form=form, page_data=page_data, pages_num = pages_num)    




def ChineseZodiac(year):
    z_dict = ("Monkey","Rooster","Dog","Pig","Rat","Ox","Tiger","Rabbit","Dragon","Snake","Horse","Sheep")
    result_cz = []
    if  z_dict[year%12] == "Monkey":
        Czodiac = "Always being smart, clever and intelligent, especially in the career and wealth. You are lively, flexible, quick-witted and versatile. In addition, your gentleness and honesty bring you an everlasting love life. Although you were born with enviable skills, you still have several shortcomings, such as an impetuous temper and a tendency to look down upon others."
        result_cz.append(Czodiac)
        Strengths = "Enthusiastic, self-assured, sociable, innovative"
        result_cz.append(Strengths)
        Weaknesses = "Jealous, suspicious, cunning, selfish, arrogant"
        result_cz.append(Weaknesses)
        Jobs = "Linguist, diplomats, journalists, entertainers, businessmen, professional athletes, stockbrokers, detectives, lawyers, programmers…"
        result_cz.append(Jobs)
        Lnumbers = "1, 7, 8"
        result_cz.append(Lnumbers)
        Lcolors = "White, gold, blue"
        result_cz.append(Lcolors)
        Lflowers = "Chrysanthemum, alliums"
        result_cz.append(Lflowers)
        Ldirection = "North, northwest, west"
        result_cz.append(Ldirection)
        result_cz.append("Monkey")
    elif z_dict[year%12] == "Rooster":
        Czodiac = "You have many excellent characteristics, such as being honest, bright, communicative and ambitious. You are born pretty or handsome, and prefer to dress up. In daily life, you seldom rely on others. However, you might be enthusiastic about something quickly, but soon be impassive. Thus, you need to have enough faiths and patience to insist on one thing."
        result_cz.append(Czodiac)
        Strengths = "Independent, capable, warm-hearted, self-respect, quick minded"
        result_cz.append(Strengths)
        Weaknesses = "Impatient, critical, eccentric, narrow-minded, selfish"
        result_cz.append(Weaknesses)
        Jobs = "Politicians, diplomats, public speakers, clothing designers, beauticians, tour guides, actors/ actresses, comedians, scientists…"
        result_cz.append(Jobs)
        Lnumbers = "5, 7, 8"
        result_cz.append(Lnumbers)
        Lcolors = "Gold, brown, brownish yellow, yellow"
        result_cz.append(Lcolors)
        Lflowers = "Gladiola, impatiens, cockscomb"
        result_cz.append(Lflowers)
        Ldirection = "West, southwest, northeast"
        result_cz.append(Ldirection)
        result_cz.append("Rooster")
    elif z_dict[year%12] == "Dog":
        Czodiac = "You are usually independent, sincere, loyal and decisive. You are not afraid of difficulties in daily life. These shining characteristics make you have harmonious relationship with people around."
        result_cz.append(Czodiac)
        Strengths = "Valiant, loyal, responsible, clever, courageous, lively"
        result_cz.append(Strengths)
        Weaknesses = "Impatient, critical, eccentric, narrow-minded, selfish"
        result_cz.append(Weaknesses)
        Jobs = "Lawyers, judges, organizers, teachers, doctors, civil servants, programmers, advertising planners, bloggers…"
        result_cz.append(Jobs)
        Lnumbers = "3, 4, 9"
        result_cz.append(Lnumbers)
        Lcolors = "Green, red, purple"
        result_cz.append(Lcolors)
        Lflowers = "Rose, oncidium, cymbidium orchids"
        result_cz.append(Lflowers)
        Ldirection = "East, southeast, south"
        result_cz.append(Ldirection)  
        result_cz.append("Dog") 
    elif z_dict[year%12] == "Pig":
        Czodiac = "You are considerate, responsible, independent and optimistic. You always show generousness and mercy to endure other people's mistakes, which help them gain harmonious interpersonal relationships. However, sometimes You will behave lazy and lack actions. In addition, pure hearts would let you be cheated easily in daily life. "
        result_cz.append(Czodiac)
        Strengths = "Warm-hearted, good-tempered, loyal, honest, gentle"
        result_cz.append(Strengths)
        Weaknesses = "Naive, gullible, sluggish, short-tempered"
        result_cz.append(Weaknesses)
        Jobs = "Veterinarians, foresters, teachers, civil servants, policemen, doctors, breeders, professors, artists…"
        result_cz.append(Jobs)
        Lnumbers = "2, 5, 8"
        result_cz.append(Lnumbers)
        Lcolors = "Yellow, grey, brown, gold"
        result_cz.append(Lcolors)
        Lflowers = "Hydrangea, pitcher plant, marguerite"
        result_cz.append(Lflowers)
        Ldirection = "Southeast, northeast"
        result_cz.append(Ldirection)  
        result_cz.append("Pig") 
    elif z_dict[year%12] == "Rat":
        Czodiac = "You are instinctive, acute and alert in nature which makes you to be brilliant businessmen. You can always react properly before the worst circumstances take place. You are also sophisticated and popular in social interaction. You are sanguine and very adaptable, being popular with others."
        result_cz.append(Czodiac)
        Strengths = "Adaptable, smart, cautious, acute, alert, positive, flexible, outgoing, cheerful"
        result_cz.append(Strengths)
        Weaknesses = "Timid, unstable, stubborn, picky, lack of persistence, querulous"
        result_cz.append(Weaknesses)
        Jobs = "Artist, author, doctor, teacher..."
        result_cz.append(Jobs)
        Lnumbers = "2, 3"
        result_cz.append(Lnumbers)
        Lcolors = "Gold, blue, green"
        result_cz.append(Lcolors)
        Lflowers = "Lily, African violet, lily of the valley"
        result_cz.append(Lflowers)
        Ldirection = "Southeast, northeast"
        result_cz.append(Ldirection) 
        result_cz.append("Rat")
    elif z_dict[year%12] == "Ox":
        Czodiac = "You bear persistent, simple, honest, and straightforward characteristics. You are talent leaders with strong faith, and strong devotion to work. You are contemplative before taking actions, not easily affected by the surroundings but just follow Your concept and ability. Being conservative with a lack of wit in speaking, You usually look silent and sometimes stubborn in your old ways."
        result_cz.append(Czodiac)
        Strengths = "Honest, industrious, patient, cautious, level-headed, strong-willed, persistent"
        result_cz.append(Strengths)
        Weaknesses = "Obstinate, inarticulate, prudish, distant"
        result_cz.append(Weaknesses)
        Jobs = "Lawyer, doctor, teacher, technician, politician, office clerk, consultant..."
        result_cz.append(Jobs)
        Lnumbers = "1, 9"
        result_cz.append(Lnumbers)
        Lcolors = "red, blue, purple"
        result_cz.append(Lcolors)
        Lflowers = "Tulip, evergreen, peach blossom"
        result_cz.append(Lflowers)
        Ldirection = "Southeast, south and north"
        result_cz.append(Ldirection) 
        result_cz.append("Ox") 
    elif z_dict[year%12] == "Tiger":
        Czodiac = "You are powerful, independent, confident and brave. You have strong sense of errantry, being frank and easy to win others' trust. In your middle age, your fate may be uneven, but after hardships, you will enjoy a bright prospect. While you are also likely to be dogmatic, and like showing off when accomplishing something."
        result_cz.append(Czodiac)
        Strengths = "Tolerant, loyal, valiant, courageous, trustworthy, intelligent, virtuous"
        result_cz.append(Strengths)
        Weaknesses = "Arrogant, short-tempered, hasty, traitorous"
        result_cz.append(Weaknesses)
        Jobs = "Economist, politician, adventurer, management officer..."
        result_cz.append(Jobs)
        Lnumbers = "1, 3, 4"
        result_cz.append(Lnumbers)
        Lcolors = "Grey, blue, white, orange"
        result_cz.append(Lcolors)
        Lflowers = "Cineraria, anthurium"
        result_cz.append(Lflowers)
        Ldirection = "South, east, southeast"
        result_cz.append(Ldirection) 
        result_cz.append("Tiger")  
    elif z_dict[year%12] == "Rabbit":
        Czodiac = "You usually impress others with an image of tenderness, grace and sensitive. You are romantic in relationship, having a high demand in life quality. You avoid arguing with others, and have a capability of converting an enemy into a friend. You are homebody and hospitable, and like house fitting-up. You can work with speed and efficiency, do not insist and get angry easily. But you also like hesitating, which makes you lose many chances."
        result_cz.append(Czodiac)
        Strengths = "Gentle, sensitive, compassionate, amiable, modest, and merciful"
        result_cz.append(Strengths)
        Weaknesses = "Amorous, hesitant, stubborn, timid, conservative"
        result_cz.append(Weaknesses)
        Jobs = "Breeder, teacher, priest, police and  judge..."
        result_cz.append(Jobs)
        Lnumbers = "3, 4, 9"
        result_cz.append(Lnumbers)
        Lcolors = "Red, blue, pink, purple"
        result_cz.append(Lcolors)
        Lflowers = "Snapdragon, plantain lily, nerve plant"
        result_cz.append(Lflowers)
        Ldirection = "East, southeast, southt"
        result_cz.append(Ldirection) 
        result_cz.append("Tiger") 
    elif z_dict[year%12] == "Dragon":
        Czodiac = "You are usually lively, intellectual and excitable. You can clearly tell right from wrong. You are upright and frank. However, you are also a bit arrogant and impatient. Sometimes you tend to be overly confident. You hate hypocrisy, gossip and slander. You are not afraid of difficulties but hate to be used or controlled by others."
        result_cz.append(Czodiac)
        Strengths = "Decisive, inspiring, magnanimous, sensitive, ambitious, romantic"
        result_cz.append(Strengths)
        Weaknesses = "Eccentric, tactless, fiery, intolerant, unrealistic"
        result_cz.append(Weaknesses)
        Jobs = "quality inspectors, cashier, financier, pharmacist, electrician, politician and priest ..."
        result_cz.append(Jobs)
        Lnumbers = "1, 7, 6"
        result_cz.append(Lnumbers)
        Lcolors = "Gold, silver, hoary"
        result_cz.append(Lcolors)
        Lflowers = "Bleeding heart vine, larkspur, hyacinth"
        result_cz.append(Lflowers)
        Ldirection = "West, north, northwest"
        result_cz.append(Ldirection)
        result_cz.append("Dragon") 
    elif z_dict[year%12] == "Snake":
        Czodiac = "You are usually sensitive and humorous, and  also gifted in literature and art. Suspicion is Your weakness, which makes you hesitant and a bit paranoid."
        result_cz.append(Czodiac)
        Strengths = "Soft-spoken, humorous, sympathetic, determined, passionate, smart"
        result_cz.append(Strengths)
        Weaknesses = "Jealous, suspicious, sly, fickle, nonchalant"
        result_cz.append(Weaknesses)
        Jobs = "Artist, politician, teacher, painter, psychologist..."
        result_cz.append(Jobs)
        Lnumbers = "2, 8, 9"
        result_cz.append(Lnumbers)
        Lcolors = "Red, light yellow, black"
        result_cz.append(Lcolors)
        Lflowers = "Orchid, cactus"
        result_cz.append(Lflowers)
        Ldirection = "Northeast, southwest, south"
        result_cz.append(Ldirection)
        result_cz.append("Snake")   
    elif z_dict[year%12] == "Horse":
        Czodiac = "You always impress upon people with dynamic, zealous and generous image. Although endowed with many shinning points, you have to face the weaknesses in their characteristics."
        result_cz.append(Czodiac)
        Strengths = "Warm-hearted, upright, easygoing, independence, endurance"
        result_cz.append(Strengths)
        Weaknesses = "Extravagant, Easy to give up"
        result_cz.append(Weaknesses)
        Jobs = "Adventurers, writers, architects, businessmen, performers, entrepreneurs, scientists, artist, politicians, critics, tour guide..."
        result_cz.append(Jobs)
        Lnumbers = "2, 3, 7"
        result_cz.append(Lnumbers)
        Lcolors = "Brown, yellow, purple"
        result_cz.append(Lcolors)
        Lflowers = "Calla lily, jasmine, marigold"
        result_cz.append(Lflowers)
        Ldirection = "Northeast, southwest and northwest"
        result_cz.append(Ldirection) 
        result_cz.append("Horse") 
    elif z_dict[year%12] == "Sheep":
        Czodiac = "You are usually tender, polite, filial, clever, and kind-hearted. You have special sensitivity to art and beauty and a special fondness for quiet living. You are wise, gentle and compassionate and can cope with business cautiously and circumspectly. In your daily life, you try to be economical. You are willing to take good care of others, but you should avoid pessimism and hesitation."
        result_cz.append(Czodiac)
        Strengths = "Gentle, softhearted, considerate, attractive, hardworking, persistent, thrift"
        result_cz.append(Strengths)
        Weaknesses = "Indecisive, timid, vain, pessimistic, moody, weak-willed"
        result_cz.append(Weaknesses)
        Jobs = "Painters, musicians, beauticians, doctors, teachers, editors, writers, typesetters, house cleaner…"
        result_cz.append(Jobs)
        Lnumbers = "3, 4, 9"
        result_cz.append(Lnumbers)
        Lcolors = "Green, red, purple"
        result_cz.append(Lcolors)
        Lflowers = "Carnation, primrose, Alice flower"
        result_cz.append(Lflowers)
        Ldirection = "East, southeast, south"
        result_cz.append(Ldirection)
        result_cz.append("Sheep")                                       
    return result_cz

def Zodiac(month,day):
    zodiac_dict = ("Capricorn","Aquarius","Pisces","Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn")
    dates = (20, 19, 21, 20, 21, 21, 23, 23, 23, 23, 22, 22)
    result_z = []
    if day < dates[month-1]:
        if zodiac_dict[month-1] == "Capricorn":
            Zodiac = "Your zodiac is Capricorn, which is a sign that represents time and responsibility, and its representatives are traditional and often very serious by nature. These individuals possess an inner state of independence that enables significant progress both in their personal and professional lives. You are masters of self-control and have the ability to lead the way, make solid and realistic plans, and manage many people who work for them at any time. You will learn from your mistakes and get to the top based solely on your experience and expertise."
            result_z.append(Zodiac)
            Strengths = "Responsible, disciplined, self-control, good managers"
            result_z.append(Strengths)
            Weaknesses = "Know-it-all, unforgiving, condescending, expecting the worst"
            result_z.append(Weaknesses)
            Likes = "Family, tradition, music, understated status, quality craftsmanship"
            result_z.append(Likes)
            Dislikes = "Almost everything at some point"
            result_z.append(Dislikes)
            result_z.append("Capricorn")
        elif zodiac_dict[month-1] == "Aquarius":
            Zodiac = "Your zodiac is Aquarius, aquarius-born are shy and quiet , but on the other hand you can be eccentric and energetic. However, in both cases, you are deep thinkers and highly intellectual people who love helping others. You are able to see without prejudice, on both sides, which makes them people who can easily solve problems. Although you can easily adapt to the energy that surrounds you, Aquarius-born have a deep need to be some time alone and away from everything, in order to restore power. People born under the Aquarius sign, look at the world as a place full of possibilities."
            result_z.append(Zodiac)
            Strengths = "Progressive, original, independent, humanitarian"
            result_z.append(Strengths)
            Weaknesses = "Runs from emotional expression, temperamental, uncompromising, aloof"
            result_z.append(Weaknesses)
            Likes = "Fun with friends, helping others, fighting for causes, intellectual conversation, a good listener"
            result_z.append(Likes)
            Dislikes = "Limitations, broken promises, being lonely, dull or boring situations, people who disagree with them"
            result_z.append(Dislikes)
            result_z.append("Aquarius")
        elif zodiac_dict[month-1] == "Pisces":
            Zodiac = "Your zodiac is Pisces, you are usually very friendly, so you often find yourselves in a company of very different people. Pisces are selfless, you are always willing to help others, without hoping to get anything back. Pisces is a Water sign and as such this zodiac sign is characterized by empathy and expressed emotional capacity."
            result_z.append(Zodiac)
            Strengths = "Compassionate, artistic, intuitive, gentle, wise, musical"
            result_z.append(Strengths)
            Weaknesses = "Fearful, overly trusting, sad, desire to escape reality, can be a victim or a martyr"
            result_z.append(Weaknesses)
            Likes = "Being alone, sleeping, music, romance, visual media, swimming, spiritual themes"
            result_z.append(Likes)
            Dislikes = "Know-it-all, being criticized, the past coming back to haunt, cruelty of any kind"
            result_z.append(Dislikes)
            result_z.append("Pisces")
        elif zodiac_dict[month-1] == "Aries":
            Zodiac = "Your zodiac is Aries, you are continuously looking for dynamic, speed and competition, always being the first in everything - from work to social gatherings. Thanks to its ruling planet Mars and the fact it belongs to the element of Fire, Aries is one of the most active zodiac signs. It is in your nature to take action, sometimes before you think about it well. The Sun in such high dignity gives them excellent organizational skills, so you'll rarely meet an Aries who isn't capable of finishing several things at once, often before lunch break! Your challenges show when you get impatient, aggressive and vent anger pointing it to other people. Strong personalities born under this sign have a task to fight for their goals, embracing togetherness and teamwork through this incarnation."
            result_z.append(Zodiac)
            Strengths = "Courageous, determined, confident, enthusiastic, optimistic, honest, passionate"
            result_z.append(Strengths)
            Weaknesses = "Impatient, moody, short-tempered, impulsive, aggressive"
            result_z.append(Weaknesses)
            Likes = "Comfortable clothes, taking on leadership roles, physical challenges, individual sports"
            result_z.append(Likes)
            Dislikes = "Inactivity, delays, work that does not use one's talents"
            result_z.append(Dislikes)
            result_z.append("Aries")    
        elif zodiac_dict[month-1] == "Taurus":
            Zodiac = "Your zodiac is Taurus. Practical and well-grounded, Taurus is the sign that harvests the fruits of labor. You feel the need to always be surrounded by love and beauty, turned to the material world, hedonism, and physical pleasures. People born with their Sun in Taurus are sensual and tactile, considering touch and taste the most important of all senses. Stable and conservative, this is one of the most reliable signs of the zodiac, ready to endure and stick to your choices until you reach the point of personal satisfaction."
            result_z.append(Zodiac)
            Strengths = "Reliable, patient, practical, devoted, responsible, stable"
            result_z.append(Strengths)
            Weaknesses = "Stubborn, possessive, uncompromising"
            result_z.append(Weaknesses)
            Likes = "Gardening, cooking, music, romance, high quality clothes, working with hands"
            result_z.append(Likes)
            Dislikes = "Sudden changes, complications, insecurity of any kind, synthetic fabrics"
            result_z.append(Dislikes)  
            result_z.append("Taurus")
        elif zodiac_dict[month-1] == "Gemini":
            Zodiac = "Your zodiac is Gemini. Expressive and quick-witted, Gemini represents two different personalities in one and you will never be sure which one you will face. You are sociable, communicative and ready for fun, with a tendency to suddenly get serious, thoughtful and restless. You are fascinated with the world itself, extremely curious, with a constant feeling that there is not enough time to experience everything you want to see."
            result_z.append(Zodiac)
            Strengths = "Gentle, affectionate, curious, adaptable, ability to learn quickly and exchange ideas"
            result_z.append(Strengths)
            Weaknesses = "Nervous, inconsistent, indecisive"
            result_z.append(Weaknesses)
            Likes = "Music, books, magazines, chats with nearly anyone, short trips around the town"
            result_z.append(Likes)
            Dislikes = "Being alone, being confined, repetition and routine"
            result_z.append(Dislikes)    
            result_z.append("Gemini")   
        elif zodiac_dict[month-1] == "Cancer":
            Zodiac = "Your zodiac is Cancer. Deeply intuitive and sentimental, Cancer can be one of the most challenging zodiac signs to get to know. You are very emotional and sensitive, and care deeply about matters of the family and your home. Cancer is sympathetic and attached to people they keep close. Those born with their Sun in Cancer are very loyal and able to empathize with other people's pain and suffering. Lack of patience or even love will manifest through mood swings later in life, and even selfishness, self-pity or manipulation. You are quick to help others, just as you are quick to avoid conflict, and rarely benefit from close combat of any kind, always choosing to hit someone stronger, bigger, or more powerful than you imagined. When at peace with your life choices, Cancer representatives will be happy and content to be surrounded by a loving family and harmony in your home."
            result_z.append(Zodiac)
            Strengths = "Tenacious, highly imaginative, loyal, emotional, sympathetic, persuasive"
            result_z.append(Strengths)
            Weaknesses = "Moody, pessimistic, suspicious, manipulative, insecure"
            result_z.append(Weaknesses)
            Likes = "Art, home-based hobbies, relaxing near or in water, helping loved ones, a good meal with friends"
            result_z.append(Likes)
            Dislikes = "Strangers, any criticism of Mom, revealing of personal life"
            result_z.append(Dislikes)  
            result_z.append("Cancer")
        elif zodiac_dict[month-1] == "Leo":
            Zodiac = "Your zodiac is Leo. People born under the sign of Leo are natural born leaders. You are dramatic, creative, self-confident, dominant and extremely difficult to resist, able to achieve anything they want to in any area of life they commit to. There is a specific strength to a Leo and your \"king of the jungle\" status. Leo often has many friends for you are generous and loyal. Self-confident and attractive, this is a Sun sign capable of uniting different groups of people and leading you as one towards a shared cause, and your healthy sense of humor makes collaboration with other people even easier."
            result_z.append(Zodiac)
            Strengths = "Creative, passionate, generous, warm-hearted, cheerful, humorous"
            result_z.append(Strengths)
            Weaknesses = "Arrogant, stubborn, self-centered, lazy, inflexible"
            result_z.append(Weaknesses)
            Likes = "Theater, taking holidays, being admired, expensive things, bright colors, fun with friends"
            result_z.append(Likes)
            Dislikes = "Being ignored, facing difficult reality, not being treated like a king or queen"
            result_z.append(Dislikes)   
            result_z.append("Leo")
        elif zodiac_dict[month-1] == "Virgo":
            Zodiac = "Your zodiac is Virgo. Virgos are always paying attention to the smallest details and their deep sense of humanity makes them one of the most careful signs of the zodiac. Your methodical approach to life ensures that nothing is left to chance, and although you are often tender, your heart might be closed for the outer world. This is a sign often misunderstood, not because you lack the ability to express, but because you won’t accept your feelings as valid, true, or even relevant when opposed to reason. The symbolism behind the name speaks well of your nature, born with a feeling you are experiencing everything for the first time."
            result_z.append(Zodiac)
            Strengths = "Loyal, analytical, kind, hardworking, practical"
            result_z.append(Strengths)
            Weaknesses = "Shyness, worry, overly critical of self and others, all work and no play"
            result_z.append(Weaknesses)
            Likes = "Animals, healthy food, books, nature, cleanliness"
            result_z.append(Likes)
            Dislikes = "Rudeness, asking for help, taking center stage"
            result_z.append(Dislikes) 
            result_z.append("Virgo")
        elif zodiac_dict[month-1] == "Libra":
            Zodiac = "Your zodiac is Libra. People born under the sign of Libra are peaceful, fair, and you hate being alone. Partnership is very important for you, as your mirror and someone giving you the ability to be the mirror yourselves. These individuals are fascinated by balance and symmetry, you are in a constant chase for justice and equality, realizing through life that the only thing that should be truly important to yourselves in your own inner core of personality. This is someone ready to do nearly anything to avoid conflict, keeping the peace whenever possible"
            result_z.append(Zodiac)
            Strengths = "Cooperative, diplomatic, gracious, fair-minded, social"
            result_z.append(Strengths)
            Weaknesses = "Indecisive, avoids confrontations, will carry a grudge, self-pity"
            result_z.append(Weaknesses)
            Likes = "Harmony, gentleness, sharing with others, the outdoors"
            result_z.append(Likes)
            Dislikes = "Violence, injustice, loudmouths, conformity"
            result_z.append(Dislikes)  
            result_z.append("Libra")
        elif zodiac_dict[month-1] == "Scorpio":
            Zodiac = "Your zodiac is Scorpio. Scorpio-born are passionate and assertive people. You are determined and decisive, and will research until you find out the truth. Scorpio is a great leader, always aware of the situation and also features prominently in resourcefulness. Scorpio is a Water sign and lives to experience and express emotions. Although emotions are very important for Scorpio, you manifest you differently than other water signs. In any case, you can keep others’ secrets, whatever they may be."
            result_z.append(Zodiac)
            Strengths = "Resourceful, brave, passionate, stubborn, a true friend"
            result_z.append(Strengths)
            Weaknesses = "Distrusting, jealous, secretive, violent"
            result_z.append(Weaknesses)
            Likes = "Truth, facts, being right, longtime friends, teasing, a grand passion"
            result_z.append(Likes)
            Dislikes = "Dishonesty, revealing secrets, passive people"
            result_z.append(Dislikes)
            result_z.append("Scorpio") 
        elif zodiac_dict[month-1] == "Sagittarius":
            Zodiac = "Your zodiac is Sagittarius. Curious and energetic, Sagittarius is one of the biggest travelers among all zodiac signs. Your open mind and philosophical view motivates you to wander around the world in search of the meaning of life. Sagittarius is extrovert, optimistic and enthusiastic, and likes changes. Sagittarius-born are able to transform your thoughts into concrete actions and you will do anything to achieve your goals."
            result_z.append(Zodiac)
            Strengths = "Generous, idealistic, great sense of humor"
            result_z.append(Strengths)
            Weaknesses = "Promises more than can deliver, very impatient, will say anything no matter how undiplomatic"
            result_z.append(Weaknesses)
            Likes = "Freedom, travel, philosophy, being outdoors"
            result_z.append(Likes)
            Dislikes = "Clingy people, being constrained, off-the-wall theories, details"
            result_z.append(Dislikes)   
            result_z.append("Sagittarius")                           
    else:
        if zodiac_dict[month] == "Capricorn":
            Zodiac = "Your zodiac is Capricorn, which is a sign that represents time and responsibility, and its representatives are traditional and often very serious by nature. These individuals possess an inner state of independence that enables significant progress both in their personal and professional lives. You are masters of self-control and have the ability to lead the way, make solid and realistic plans, and manage many people who work for them at any time. You will learn from your mistakes and get to the top based solely on your experience and expertise."
            result_z.append(Zodiac)
            Strengths = "Responsible, disciplined, self-control, good managers"
            result_z.append(Strengths)
            Weaknesses = "Know-it-all, unforgiving, condescending, expecting the worst"
            result_z.append(Weaknesses)
            Likes = "Family, tradition, music, understated status, quality craftsmanship"
            result_z.append(Likes)
            Dislikes = "Almost everything at some point"
            result_z.append(Dislikes)
            result_z.append("Capricorn")
        elif zodiac_dict[month] == "Aquarius":
            Zodiac = "Your zodiac is Aquarius, aquarius-born are shy and quiet , but on the other hand you can be eccentric and energetic. However, in both cases, you are deep thinkers and highly intellectual people who love helping others. You are able to see without prejudice, on both sides, which makes them people who can easily solve problems. Although you can easily adapt to the energy that surrounds you, Aquarius-born have a deep need to be some time alone and away from everything, in order to restore power. People born under the Aquarius sign, look at the world as a place full of possibilities."
            result_z.append(Zodiac)
            Strengths = "Progressive, original, independent, humanitarian"
            result_z.append(Strengths)
            Weaknesses = "Runs from emotional expression, temperamental, uncompromising, aloof"
            result_z.append(Weaknesses)
            Likes = "Fun with friends, helping others, fighting for causes, intellectual conversation, a good listener"
            result_z.append(Likes)
            Dislikes = "Limitations, broken promises, being lonely, dull or boring situations, people who disagree with them"
            result_z.append(Dislikes)
            result_z.append("Aquarius")
        elif zodiac_dict[month] == "Pisces":
            Zodiac = "Your zodiac is Pisces, you are usually very friendly, so you often find yourselves in a company of very different people. Pisces are selfless, you are always willing to help others, without hoping to get anything back. Pisces is a Water sign and as such this zodiac sign is characterized by empathy and expressed emotional capacity."
            result_z.append(Zodiac)
            Strengths = "Compassionate, artistic, intuitive, gentle, wise, musical"
            result_z.append(Strengths)
            Weaknesses = "Fearful, overly trusting, sad, desire to escape reality, can be a victim or a martyr"
            result_z.append(Weaknesses)
            Likes = "Being alone, sleeping, music, romance, visual media, swimming, spiritual themes"
            result_z.append(Likes)
            Dislikes = "Know-it-all, being criticized, the past coming back to haunt, cruelty of any kind"
            result_z.append(Dislikes)
            result_z.append("Pisces")
        elif zodiac_dict[month] == "Aries":
            Zodiac = "Your zodiac is Aries, you are continuously looking for dynamic, speed and competition, always being the first in everything - from work to social gatherings. Thanks to its ruling planet Mars and the fact it belongs to the element of Fire, Aries is one of the most active zodiac signs. It is in your nature to take action, sometimes before you think about it well. The Sun in such high dignity gives them excellent organizational skills, so you'll rarely meet an Aries who isn't capable of finishing several things at once, often before lunch break! Your challenges show when you get impatient, aggressive and vent anger pointing it to other people. Strong personalities born under this sign have a task to fight for their goals, embracing togetherness and teamwork through this incarnation."
            result_z.append(Zodiac)
            Strengths = "Courageous, determined, confident, enthusiastic, optimistic, honest, passionate"
            result_z.append(Strengths)
            Weaknesses = "Impatient, moody, short-tempered, impulsive, aggressive"
            result_z.append(Weaknesses)
            Likes = "Comfortable clothes, taking on leadership roles, physical challenges, individual sports"
            result_z.append(Likes)
            Dislikes = "Inactivity, delays, work that does not use one's talents"
            result_z.append(Dislikes)   
            result_z.append("Aries") 
        elif zodiac_dict[month] == "Taurus":
            Zodiac = "Your zodiac is Taurus. Practical and well-grounded, Taurus is the sign that harvests the fruits of labor. You feel the need to always be surrounded by love and beauty, turned to the material world, hedonism, and physical pleasures. People born with their Sun in Taurus are sensual and tactile, considering touch and taste the most important of all senses. Stable and conservative, this is one of the most reliable signs of the zodiac, ready to endure and stick to your choices until you reach the point of personal satisfaction."
            result_z.append(Zodiac)
            Strengths = "Reliable, patient, practical, devoted, responsible, stable"
            result_z.append(Strengths)
            Weaknesses = "Stubborn, possessive, uncompromising"
            result_z.append(Weaknesses)
            Likes = "Gardening, cooking, music, romance, high quality clothes, working with hands"
            result_z.append(Likes)
            Dislikes = "Sudden changes, complications, insecurity of any kind, synthetic fabrics"
            result_z.append(Dislikes)  
            result_z.append("Taurus")
        elif zodiac_dict[month] == "Gemini":
            Zodiac = "Your zodiac is Gemini. Expressive and quick-witted, Gemini represents two different personalities in one and you will never be sure which one you will face. You are sociable, communicative and ready for fun, with a tendency to suddenly get serious, thoughtful and restless. You are fascinated with the world itself, extremely curious, with a constant feeling that there is not enough time to experience everything you want to see."
            result_z.append(Zodiac)
            Strengths = "Gentle, affectionate, curious, adaptable, ability to learn quickly and exchange ideas"
            result_z.append(Strengths)
            Weaknesses = "Nervous, inconsistent, indecisive"
            result_z.append(Weaknesses)
            Likes = "Music, books, magazines, chats with nearly anyone, short trips around the town"
            result_z.append(Likes)
            Dislikes = "Being alone, being confined, repetition and routine"
            result_z.append(Dislikes)     
            result_z.append("Gemini")  
        elif zodiac_dict[month] == "Cancer":
            Zodiac = "Your zodiac is Cancer. Deeply intuitive and sentimental, Cancer can be one of the most challenging zodiac signs to get to know. You are very emotional and sensitive, and care deeply about matters of the family and your home. Cancer is sympathetic and attached to people they keep close. Those born with their Sun in Cancer are very loyal and able to empathize with other people's pain and suffering. Lack of patience or even love will manifest through mood swings later in life, and even selfishness, self-pity or manipulation. You are quick to help others, just as you are quick to avoid conflict, and rarely benefit from close combat of any kind, always choosing to hit someone stronger, bigger, or more powerful than you imagined. When at peace with your life choices, Cancer representatives will be happy and content to be surrounded by a loving family and harmony in your home."
            result_z.append(Zodiac)
            Strengths = "Tenacious, highly imaginative, loyal, emotional, sympathetic, persuasive"
            result_z.append(Strengths)
            Weaknesses = "Moody, pessimistic, suspicious, manipulative, insecure"
            result_z.append(Weaknesses)
            Likes = "Art, home-based hobbies, relaxing near or in water, helping loved ones, a good meal with friends"
            result_z.append(Likes)
            Dislikes = "Strangers, any criticism of Mom, revealing of personal life"
            result_z.append(Dislikes)  
            result_z.append("Cancer")
        elif zodiac_dict[month] == "Leo":
            Zodiac = "Your zodiac is Leo. People born under the sign of Leo are natural born leaders. You are dramatic, creative, self-confident, dominant and extremely difficult to resist, able to achieve anything they want to in any area of life they commit to. There is a specific strength to a Leo and your \"king of the jungle\" status. Leo often has many friends for you are generous and loyal. Self-confident and attractive, this is a Sun sign capable of uniting different groups of people and leading you as one towards a shared cause, and your healthy sense of humor makes collaboration with other people even easier."
            result_z.append(Zodiac)
            Strengths = "Creative, passionate, generous, warm-hearted, cheerful, humorous"
            result_z.append(Strengths)
            Weaknesses = "Arrogant, stubborn, self-centered, lazy, inflexible"
            result_z.append(Weaknesses)
            Likes = "Theater, taking holidays, being admired, expensive things, bright colors, fun with friends"
            result_z.append(Likes)
            Dislikes = "Being ignored, facing difficult reality, not being treated like a king or queen"
            result_z.append(Dislikes)  
            result_z.append("Leo") 
        elif zodiac_dict[month] == "Virgo":
            Zodiac = "Your zodiac is Virgo. Virgos are always paying attention to the smallest details and their deep sense of humanity makes them one of the most careful signs of the zodiac. Your methodical approach to life ensures that nothing is left to chance, and although you are often tender, your heart might be closed for the outer world. This is a sign often misunderstood, not because you lack the ability to express, but because you won’t accept your feelings as valid, true, or even relevant when opposed to reason. The symbolism behind the name speaks well of your nature, born with a feeling you are experiencing everything for the first time."
            result_z.append(Zodiac)
            Strengths = "Loyal, analytical, kind, hardworking, practical"
            result_z.append(Strengths)
            Weaknesses = "Shyness, worry, overly critical of self and others, all work and no play"
            result_z.append(Weaknesses)
            Likes = "Animals, healthy food, books, nature, cleanliness"
            result_z.append(Likes)
            Dislikes = "Rudeness, asking for help, taking center stage"
            result_z.append(Dislikes) 
            result_z.append("Virgo")
        elif zodiac_dict[month] == "Libra":
            Zodiac = "Your zodiac is Libra. People born under the sign of Libra are peaceful, fair, and you hate being alone. Partnership is very important for you, as your mirror and someone giving you the ability to be the mirror yourselves. These individuals are fascinated by balance and symmetry, you are in a constant chase for justice and equality, realizing through life that the only thing that should be truly important to yourselves in your own inner core of personality. This is someone ready to do nearly anything to avoid conflict, keeping the peace whenever possible"
            result_z.append(Zodiac)
            Strengths = "Cooperative, diplomatic, gracious, fair-minded, social"
            result_z.append(Strengths)
            Weaknesses = "Indecisive, avoids confrontations, will carry a grudge, self-pity"
            result_z.append(Weaknesses)
            Likes = "Harmony, gentleness, sharing with others, the outdoors"
            result_z.append(Likes)
            Dislikes = "Violence, injustice, loudmouths, conformity"
            result_z.append(Dislikes)  
            result_z.append("Libra")
        elif zodiac_dict[month] == "Scorpio":
            Zodiac = "Your zodiac is Scorpio. Scorpio-born are passionate and assertive people. You are determined and decisive, and will research until you find out the truth. Scorpio is a great leader, always aware of the situation and also features prominently in resourcefulness. Scorpio is a Water sign and lives to experience and express emotions. Although emotions are very important for Scorpio, you manifest you differently than other water signs. In any case, you can keep others’ secrets, whatever they may be."
            result_z.append(Zodiac)
            Strengths = "Resourceful, brave, passionate, stubborn, a true friend"
            result_z.append(Strengths)
            Weaknesses = "Distrusting, jealous, secretive, violent"
            result_z.append(Weaknesses)
            Likes = "Truth, facts, being right, longtime friends, teasing, a grand passion"
            result_z.append(Likes)
            Dislikes = "Dishonesty, revealing secrets, passive people"
            result_z.append(Dislikes) 
            result_z.append("Scorpio")
        elif zodiac_dict[month] == "Sagittarius":
            Zodiac = "Your zodiac is Sagittarius. Curious and energetic, Sagittarius is one of the biggest travelers among all zodiac signs. Your open mind and philosophical view motivates you to wander around the world in search of the meaning of life. Sagittarius is extrovert, optimistic and enthusiastic, and likes changes. Sagittarius-born are able to transform your thoughts into concrete actions and you will do anything to achieve your goals."
            result_z.append(Zodiac)
            Strengths = "Generous, idealistic, great sense of humor"
            result_z.append(Strengths)
            Weaknesses = "Promises more than can deliver, very impatient, will say anything no matter how undiplomatic"
            result_z.append(Weaknesses)
            Likes = "Freedom, travel, philosophy, being outdoors"
            result_z.append(Likes)
            Dislikes = "Clingy people, being constrained, off-the-wall theories, details"
            result_z.append(Dislikes)        
            result_z.append("Sagittarius")     
    return result_z   






    



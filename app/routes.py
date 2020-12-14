from flask_login import current_user, login_user
from flask_wtf import form
from sqlalchemy import JSON

from app import app, db
from flask import render_template, flash, jsonify, url_for, redirect, session

from app.forms import CreatePostForm, LoginForm, RegistrationForm, ForumForm, PostForm, ReplyForm
from app.models import User, Post, Forum, Reply


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/testpage')
def testpage():
    return render_template('testpage.html', title='Test')

@app.route('/_test')
def test():
    test = Post.query.all()
    result = list()
    for p in test:
        result.append({"title": p.title, "timestamp": p.timestamp})

    return jsonify(result=result)


@app.route('/_processforum')
def processforum():
    processforum = Forum.query.all()
    result = list()
    for p in processforum:
        result.append({"title": p.book_title, "author": p.author, "timestamp": p.timestamp})
    return jsonify(result=result)

@app.route('/_processpost')
def processpost():
    processpost = Post.query.all()
    forum = Forum.query.all()
    result = list()
    for p in processpost:
        result.append({"title": p.title, "content": p.content, "timestamp": p.timestamp})
    for f in forum:
        result.append({"book_title": f.book_title})
    return jsonify(result=result)

@app.route('/forums', methods=['GET', 'POST'])
def forums():
    forumList = Forum.query.all()
    form = ForumForm()
    if form.validate_on_submit():
        forum = Forum(userID=current_user.id, book_title=form.book_title.data, author=form.author.data)
        db.session.add(forum)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        final_form = ForumForm()

        return redirect(url_for('forums'))
        render_template('forums.html', title='New Post', form=final_form)
    return render_template('forums.html', title='New Post', form=form)

@app.route('/contact')
def contact():
    return render_template('contact.html', title= 'Contact')

#----------------------------
@app.route('/createforum', methods=['GET', 'POST'])
def createforum():
    form = ForumForm()
    if form.validate_on_submit():
        user = Forum(userID=current_user.id, book_title=form.book_title.data, author=form.author.data)
        db.session.add(user)
        db.session.commit()

        flash('Created new Post: {}'.format(
            form.book_title.data))
        final_form = ForumForm()
        render_template('createforum.html', title='New Post', form=final_form)
    return render_template('createforum.html',title='New Post', form=form)
#---------------------------

@app.route('/makepost/<book_title>', methods=['GET', 'POST'])
def makepost(book_title):
    book = Forum.query.filter_by(book_title=book_title).first()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(userID=current_user.id, forumID=book.id, title=form.title.data, content=form.content.data)
        db.session.add(post)
        db.session.commit()

        flash('Created new Post: {}'.format(
            form.title.data))
        final_form = ForumForm()
        render_template('createforum.html', title='New Post', book=book, form=final_form)
        return redirect(url_for('forum', book_title=book_title))
    return render_template('createforum.html',title='New Post', book=book, form=form)


@app.route('/reply/<book_title>/<title>', methods=['GET', 'POST'])
def reply(book_title, title):
    post = Post.query.filter_by(title=title).first()
    book = Forum.query.filter_by(book_title=book_title).first()
    form = ReplyForm()
    if form.validate_on_submit():
        reply = Reply(userID=current_user.id, postID=post.id, content=form.content.data)
        db.session.add(reply)
        db.session.commit()

        #p2r = PostToReply(postID=post.id, replyID=reply.id)
        #db.session.add(p2r)
        #db.session.commit()

        flash('Reply Successful')
        final_form = ReplyForm()
        render_template('reply.html', title='Reply', book=book, post=post, form=final_form)
        session['book'] = Forum.query.filter_by(book_title=book_title).first()
        return redirect(url_for('forum', book_title=book_title))
    return render_template('reply.html',title='Reply', book=book, post=post, form=form)


@app.route('/_createPost')
def createPost():
    post = Post.query.all()
    test= list()
    test.append("hello")
    test.append("hi")

    return jsonify(result=test)

@app.route('/forum/<book_title>', methods=['GET', 'POST'])
def forum(book_title):
    forum = Forum.query.filter_by(book_title=book_title).first()

    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data)
        db.session.add(post)
        db.session.commit()


        flash('Created new Post: {}'.format(
            form.title.data))
        final_form = CreatePostForm()
        return redirect(url_for('forum', book_title=forum.book_title))

        render_template('forum.html', title='New Post', forum=forum, form=final_form)
    return render_template('forum.html',title='New Post', forum=forum, form=form)


@app.route('/post', methods=['GET', 'POST'])
def post():

    return render_template('post.html')

@app.route('/_processlogin')
def processlogin():
    result = list()
    result.append({"title": "frog"})
    return jsonify(result=result)


@app.route('/login', methods=['GET', 'POST'])
def login():
    #if current_user.is_authenticated:
        #return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    #if current_user.is_authenticated:
        #return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now create and interact in forums')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_db')
def reset_db():
   flash("Resetting database: deleting old data and repopulating with dummy data")
   # clear all data from all tables
   meta = db.metadata
   for table in reversed(meta.sorted_tables):
       print('Clear table {}'.format(table))
       db.session.execute(table.delete())
   db.session.commit()

@app.route('/populate_db')
def populate_db():
    b1 = User(name="Jim")
    b1.set_password("Marillion")
    b2 = User(name="Gandalf")
    b2.set_password("Gandalf")
    b3 = User(name="Saruman")
    b3.set_password("Saruman")
    db.session.add_all([b1, b2, b3])
    db.session.commit()
    e1 = Forum(userID=1, book_title="Hitchhiker's Guide to the Galaxy", author="Douglas Adams")
    e2 = Forum(userID=2, book_title="The Silmarillion", author="J.R.R. Tolkien")
    e3 = Forum(userID=2, book_title="The Martian", author="Andy Weir")
    db.session.add_all([e1, e2, e3])
    db.session.commit()
    p1 = Post(title="I liked this book", content="This book is really funny!", userID=3, forumID=1)
    p2 = Post(title="Depressing", content="This book had a lot of tragic stories.", userID=2, forumID=2)
    p3 = Post(title="Cool!", content="A fine read!", userID=1, forumID=2)
    p4 = Post(title="Weir Science", content="There's a lot of science in this book!", userID=2, forumID=3)
    db.session.add_all([p1, p2, p3, p4])
    db.session.commit()
    r1 = Reply(userID=2, content="I disagree!", postID=2)
    r2 = Reply(userID=1, content="I agree!", postID=3)
    r3 = Reply(userID=3, content="I dunno.", postID=1)
    r4 = Reply(userID=1, content="huh.", postID=1)
    db.session.add_all([r1, r2, r3, r4])
    db.session.commit()

    #p1 = PostToReply(postID=1, replyID=1)
    #p2 = PostToReply(postID=1, replyID=2)
    #p3 = PostToReply(postID=1, replyID=3)
   # p4 = PostToReply(postID=1, replyID=4)
    #db.session.add_all([p1, p2, p3, p4])
    #db.session.commit()
    return render_template('base.html', title='Populate DB')

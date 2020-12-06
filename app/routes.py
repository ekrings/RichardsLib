from app import app
from flask import render_template, flash, redirect, url_for
from app import db
from app.forms import CreatePostForm
from app.models import User, Post, Forum, Reply


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/forums')
def forums():
    forumList = Forum.query.all()
    return render_template('forums.html', forumList=forumList)


@app.route('/forum/<book_title>',  methods=['GET', 'POST'])
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
        render_template('forum.html', title='New Post', forum=forum, form=final_form)
    return render_template('forum.html',title='New Post', forum=forum, form=form)


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
    db.session.add_all([r1, r2, r3])
    db.session.commit()
    return render_template('base.html', title='Populate DB')
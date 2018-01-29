from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Database for Blog Content
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/pruthivimuhilan/PycharmProjects/star/Blog1/blog.db'

db = SQLAlchemy(app)


class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)


# Static home page
@app.route('/')
def index():
    return render_template('index.html')


# Blog Listing page
@app.route('/blog')
def blog():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('blog.html', posts=posts)


# Post listing page
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    return render_template('post.html', post=post)


# Adding new post
@app.route('/add')
def add():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('add.html')


# Submitting the post added
@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('blog'))


# Login page for adding new blog post
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password')
    return add()


# Logout after posting
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return add()


# Error handling page
@app.errorhandler(404)
def page_not_found():
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True)
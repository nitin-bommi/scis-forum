from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from scisforum import app, db, bcrypt
from scisforum.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, MessageForm
from scisforum.models import User, Post, Message, Event
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import or_, and_
from PIL import Image
import os
import secrets
from scisforum.profanity_checker import predict_prob
from datetime import datetime
import dateutil.parser as dt


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created. You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():
    return render_template('login.html', title='Login')


@app.route('/login_password', methods=['GET', 'POST'])
def login_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
    return render_template('login_password.html', title='Login', form=form)


@app.route('/login_face')
def login_face():
    return render_template('login_face.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if predict_prob([form.content.data]) > 0.4:
            flash('Your post contains inappropriate words. Please filter out them.', 'danger')
            return redirect(url_for('new_post'))
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created.', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if predict_prob([form.content.data]) > 0.4:
            flash('Your post contains inappropriate words. Please filter out them.', 'danger')
            return redirect(url_for('new_post'))
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated.', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@app.route('/chatting/<string:username>', methods=['GET', 'POST'])
@login_required
def chatting(username):
    form = MessageForm(request.form)
    user = User.query.filter_by(username=username).first_or_404()
    if request.method == 'POST':
        if predict_prob([form.body.data]) > 0.4:
            flash('Your text contains inappropriate words. Please filter out them.', 'danger')
            return redirect(url_for('chatting', username=username))
        message = Message(msg_by_id=current_user.id, msg_to_id=user.id, body=form.body.data)
        db.session.add(message)
        db.session.commit()
    users = User.query.all()
    return render_template('chat_room.html', users=users, form=form, receiver=username)


@app.route('/chats/<string:username>', methods=['GET', 'POST'])
@login_required
def chats(username):
    user = User.query.filter_by(username=username).first_or_404()
    messages = Message.query.filter(or_((and_(Message.msg_by_id==user.id, Message.msg_to_id==current_user.id)), (and_(Message.msg_by_id==current_user.id, Message.msg_to_id==user.id))))
    return render_template('chats.html', title='Chat', chats=messages)

@app.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    events = Event.query.all()
    return render_template('calendar.html', title='Calendar', events=events)

@app.route("/insert_event", methods=["POST","GET"])
@login_required
def insert_event():
    if not current_user.access:
        abort(403)
    if request.method == 'POST':
        title = request.form['title']
        start_time = dt.parse(request.form['start'])
        end_time = dt.parse(request.form['end'])
        event = Event(title=title, start_time=start_time, end_time=end_time, creator_id=current_user.id)
        db.session.add(event)
        db.session.commit()
        flash('Event Created.', 'success')
        return redirect(url_for('calendar'))

@app.route("/update_event", methods=["POST","GET"])
@login_required
def update_event():
    if not current_user.access:
        abort(403)
    if request.method == 'POST':
        title = request.form['title']
        start_time = dt.parse(request.form['start'])
        end_time = dt.parse(request.form['end'])
        id = request.form['id']
        event = Event.query.get_or_404(id)
        if event.creator_id != current_user.id:
            abort(403)
        event.title = title
        event.start_time = start_time
        event.end_time = end_time
        db.session.commit()
        flash('Event updated.', 'success')
        return redirect(url_for('calendar'))

@app.route("/delete_event", methods=["POST","GET"])
@login_required
def delete_event():
    if not current_user.access:
        abort(403)
    if request.method == 'POST':
        id = request.form['id']
        event = Event.query.get_or_404(id)
        if event.creator_id != current_user.id:
            abort(403)
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted.', 'success')
        return redirect(url_for('calendar'))

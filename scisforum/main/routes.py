from flask import render_template, request, Blueprint, flash, redirect, url_for
from flask_login import current_user
from scisforum.models import Post
from scisforum.main.utils import send_message, reply_message
main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route('/about')
def about():
    return render_template('about.html', title='About')


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        message = request.form['message']
        if(message == ''):
            flash('Message is empty', 'warning')
            return redirect(url_for('main.home'))
        send_message(current_user.email, message)
        reply_message(current_user.email)
        flash('Message Sent', 'info')
    return redirect(url_for('main.home'))


@main.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    if keyword is None:
        return redirect(url_for('main.home'))
    keyword = keyword.lower()
    posts = Post.query.filter(Post.title.like(f'%{keyword}%')).paginate(page=page, per_page=5)
    # result = []
    # for post in posts:
    #     if keyword in post.title.lower():
    #         result.append(post)
    return render_template('home.html', posts=posts, keyword = keyword)
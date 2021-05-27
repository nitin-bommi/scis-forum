from flask import render_template, request, Blueprint, flash, redirect, url_for
from email_validator import validate_email, EmailNotValidError
from scisforum.models import Post
from scisforum.main.utils import send_message
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
        email = request.form['email']
        message = request.form['message']
        try:
            valid = validate_email(email)
            email = valid.email
            if(message == ''):
                flash('Message is empty', 'info')
                return redirect(url_for('main.home'))
            send_message(email, message)
            flash('Message Sent', 'info')
        except EmailNotValidError as e:
            flash('Enter valid email', 'danger')
    return redirect(url_for('main.home'))

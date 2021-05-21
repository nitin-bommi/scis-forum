from flask import render_template, request, Blueprint
import random
from scisforum.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    sidebar_posts = random.sample(Post.query.all(), 2)
    return render_template('home.html', posts=posts, sidebar_posts=sidebar_posts)


@main.route('/about')
def about():
    return render_template('about.html', title='About')
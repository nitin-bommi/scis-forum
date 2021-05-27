from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from sqlalchemy import or_, and_
from scisforum import db
from scisforum.models import User, Message
from scisforum.chats.forms import MessageForm
from scisforum.profanity_checker import predict_prob

chats = Blueprint('chats', __name__)


@chats.route('/chatting/<string:username>', methods=['GET', 'POST'])
@login_required
def chatting(username):
    form = MessageForm(request.form)
    user = User.query.filter_by(username=username).first_or_404()
    if request.method == 'POST':
        if predict_prob([form.body.data]) > 0.4:
            flash('Your text contains inappropriate words. Please filter out them.', 'danger')
            return redirect(url_for('chats.chatting', username=username))
        message = Message(msg_by_id=current_user.id, msg_to_id=user.id, body=form.body.data)
        db.session.add(message)
        db.session.commit()
    existing = Message.query.join(User, or_(User.id == Message.msg_by_id, User.id == Message.msg_to_id)).add_columns(User.username).filter(or_(Message.msg_by_id == current_user.id, Message.msg_to_id == current_user.id)).order_by(Message.msg_time.desc())
    unique = []
    for user in existing:
        if user.username != current_user.username and user.username not in unique:
            unique.append(user.username)
    users = User.query.filter(User.username.notin_([*unique, current_user.username]))
    for user in users:
        unique.append(user.username)
    return render_template('chat_room.html', users=unique, form=form, receiver=username)


@chats.route('/chats/<string:username>', methods=['GET', 'POST'])
@login_required
def chats_view(username):
    user = User.query.filter_by(username=username).first_or_404()
    messages = Message.query.filter(or_((and_(Message.msg_by_id==user.id, Message.msg_to_id==current_user.id)), (and_(Message.msg_by_id==current_user.id, Message.msg_to_id==user.id))))
    return render_template('chats.html', title='Chat', chats=messages)
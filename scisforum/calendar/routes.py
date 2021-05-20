import dateutil.parser as dt
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from scisforum import db
from scisforum.models import Event

calendar = Blueprint('calendar', __name__)


@calendar.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    events = Event.query.all()
    return render_template('calendar.html', title='Calendar', events=events)


@calendar.route("/insert_event", methods=["POST","GET"])
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
        return redirect(url_for('calendar.calendar'))


@calendar.route("/update_event", methods=["POST","GET"])
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
        return redirect(url_for('calendar.calendar'))


@calendar.route("/delete_event", methods=["POST","GET"])
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
        return redirect(url_for('calendar.calendar'))
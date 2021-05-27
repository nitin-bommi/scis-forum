from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class MessageForm(FlaskForm):
    body = StringField('', validators=[DataRequired(), Length(min=1)], render_kw={'autofocus': True})



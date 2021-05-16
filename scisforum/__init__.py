from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '53ad147a12147000dc5eed019639856e'

from scisforum import routes

from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_pyfile("../config.py")

csrf = CSRFProtect(app)

from app import views

from .users import user_bp
app.register_blueprint(user_bp)

from .products import product_bp
app.register_blueprint(product_bp)

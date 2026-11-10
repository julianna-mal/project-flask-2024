
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from app.posts import posts_bp
from app.config import config
from app.extensions import db, migrate

csrf = CSRFProtect()


def create_app(config_name="development"):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app.views import main_bp
    from app.users import user_bp
    from app.products import product_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(posts_bp)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    return app

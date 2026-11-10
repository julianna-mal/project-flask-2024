
from flask import Blueprint

posts_bp = Blueprint(
    "posts",
    __name__,
    template_folder="templates",
    url_prefix="/post"
)

from app.posts import views

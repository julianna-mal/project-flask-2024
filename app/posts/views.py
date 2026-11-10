
from datetime import datetime

from flask import render_template, redirect, url_for, flash, abort

from app.extensions import db
from app.posts import posts_bp
from app.posts.models import Post
from app.posts.forms import PostForm


@posts_bp.route("/")
def all_posts():
    posts = Post.query.filter_by(is_active=True).order_by(
        Post.posted.desc()
    ).all()

    return render_template("posts/all_posts.html", posts=posts)


@posts_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            author=form.author.data or "Anonymous",
            is_active=form.is_active.data,
            posted=form.posted.data
        )

        db.session.add(post)
        db.session.commit()

        flash("Публікацію успішно додано!", "success")
        return redirect(url_for("posts.all_posts"))

    if not form.posted.data:
        form.posted.data = datetime.now()

    return render_template(
        "posts/add_post.html",
        form=form,
        title="Додати публікацію"
    )


@posts_bp.route("/<int:post_id>")
def detail_post(post_id):
    post = db.session.get(Post, post_id)

    if post is None:
        abort(404)

    return render_template("posts/detail_post.html", post=post)


@posts_bp.route("/<int:post_id>/update", methods=["GET", "POST"])
def update_post(post_id):
    post = db.session.get(Post, post_id)

    if post is None:
        abort(404)

    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.author = form.author.data or "Anonymous"
        post.is_active = form.is_active.data
        post.posted = form.posted.data

        db.session.commit()

        flash("Публікацію оновлено!", "success")
        return redirect(url_for("posts.detail_post", post_id=post.id))

    return render_template(
        "posts/add_post.html",
        form=form,
        title="Редагувати публікацію"
    )


@posts_bp.route("/<int:post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id):
    post = db.session.get(Post, post_id)

    if post is None:
        abort(404)

    if form_submitted():
        db.session.delete(post)
        db.session.commit()

        flash("Публікацію видалено!", "success")
        return redirect(url_for("posts.all_posts"))

    return render_template("posts/delete_confirm.html", post=post)


def form_submitted():
    from flask import request
    return request.method == "POST"

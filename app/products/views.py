import os

from flask import render_template, redirect, url_for, abort, flash, request
from werkzeug.utils import secure_filename
from decimal import Decimal

from . import product_bp
from .forms import ProductForm
from .storage import (
    get_all_products,
    get_product,
    add_product,
    update_product,
    delete_product
)
from .utils import save_product_image


@product_bp.route("/")
def product_list():
    products = get_all_products()
    return render_template("products/products.html", products=products)


@product_bp.route("/add", methods=["GET", "POST"])
def product_add():
    form = ProductForm()

    if form.validate_on_submit():
        image_path = save_product_image(form.image.data)

        data = {
            "name": form.name.data,
            "content": form.content.data,
            "price": str(form.price.data),
            "category": form.category.data,
            "quantity": form.quantity.data,
            "image": image_path
        }

        add_product(data)

        flash("Товар успішно додано!", "success")
        return redirect(url_for("products.product_list"))

    return render_template("products/product_form.html", form=form, title="Додати товар")


@product_bp.route("/<int:product_id>")
def product_detail(product_id):
    product = get_product(product_id)

    if product is None:
        abort(404)

    return render_template("products/detail_product.html", product=product)


@product_bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
def product_edit(product_id):
    product = get_product(product_id)

    if product is None:
        abort(404)

    form = ProductForm()

    if form.validate_on_submit():
        image_path = product.get("image")

        if form.image.data:
            image_path = save_product_image(form.image.data)

        data = {
            "name": form.name.data,
            "content": form.content.data,
            "price": str(form.price.data),
            "category": form.category.data,
            "quantity": form.quantity.data,
            "image": image_path
        }

        update_product(product_id, data)

        flash("Товар успішно оновлено!", "success")
        return redirect(url_for("products.product_detail", product_id=product_id))

    if request.method == "GET":
        form.name.data = product["name"]
        form.content.data = product["content"]
        form.price.data = Decimal(str(product["price"]))
        form.category.data = product["category"]
        form.quantity.data = product["quantity"]

    return render_template(
        "products/product_form.html",
        form=form,
        title="Редагувати товар"
    )


@product_bp.route("/<int:product_id>/delete", methods=["POST"])
def product_delete(product_id):
    product = get_product(product_id)

    if product is None:
        abort(404)

    delete_product(product_id)

    flash("Товар видалено!", "success")
    return redirect(url_for("products.product_list"))

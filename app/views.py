
import logging
import os

from flask import render_template, request, redirect, url_for, flash
from . import app
from .forms import ContactForm


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    log_file = os.path.join(os.path.dirname(__file__), "contacts.log")
    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    ))
    logger.addHandler(handler)


@app.route('/')
@app.route('/resume')
def resume():
    return render_template('resume.html')


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()

    if form.validate_on_submit():
        try:
            logger.info(
                "Ім'я: %s | Email: %s | Тема: %s | Категорія: %s | Повідомлення: %s",
                form.name.data,
                form.email.data,
                form.subject.data,
                form.category.data,
                form.message.data
            )

            flash("Повідомлення успішно надіслано!", "success")

        except Exception:
            logger.exception("Помилка запису повідомлення")
            flash("Не вдалося надіслати повідомлення.", "danger")

        return redirect(url_for('contacts'))

    if request.method == 'POST':
        flash("Перевірте правильність заповнення форми.", "danger")

    return render_template('contacts.html', form=form)

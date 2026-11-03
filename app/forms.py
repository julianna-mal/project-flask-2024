
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField(
        "Ваше ім'я",
        validators=[DataRequired(), Length(min=2, max=50)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    subject = StringField(
        "Тема повідомлення",
        validators=[DataRequired(), Length(min=3, max=100)]
    )

    category = SelectField(
        "Категорія",
        choices=[
            ("question", "Запитання"),
            ("cooperation", "Співпраця"),
            ("other", "Інше")
        ],
        validators=[DataRequired()]
    )

    message = TextAreaField(
        "Повідомлення",
        validators=[DataRequired(), Length(min=10, max=2000)]
    )

    submit = SubmitField("Надіслати")


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateTimeLocalField


class PostForm(FlaskForm):
    title = StringField(
        "Назва",
        validators=[DataRequired(), Length(max=150)]
    )

    content = TextAreaField(
        "Текст публікації",
        validators=[DataRequired()]
    )

    category = SelectField(
        "Категорія",
        choices=[
            ("news", "Новини"),
            ("publication", "Публікації"),
            ("tech", "Технології"),
            ("other", "Інше")
        ],
        validators=[DataRequired()]
    )

    author = StringField(
        "Автор",
        default="Anonymous",
        validators=[Length(max=20)]
    )

    is_active = BooleanField("Активна публікація", default=True)

    posted = DateTimeLocalField(
        "Дата публікації",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()]
    )

    submit = SubmitField("Зберегти")

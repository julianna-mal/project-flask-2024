from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import StringField, TextAreaField, DecimalField
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductForm(FlaskForm):

    name = StringField(
        "Назва товару",
        validators=[
            DataRequired(message="Введіть назву"),
            Length(min=3, message="Мінімум 3 символи")
        ]
    )

    content = TextAreaField(
        "Опис товару",
        validators=[DataRequired(message="Введіть опис")]
    )

    price = DecimalField(
        "Ціна",
        places=2,
        validators=[
            DataRequired(message="Введіть ціну"),
            NumberRange(min=0.01, message="Ціна має бути більшою за 0")
        ]
    )

    category = SelectField(
        "Категорія",
        choices=[
            ("electronics", "Електроніка"),
            ("clothing", "Одяг"),
            ("home", "Товари для дому"),
            ("other", "Інше")
        ],
        validators=[DataRequired()]
    )

    quantity = IntegerField(
        "Кількість",
        validators=[
            DataRequired(message="Введіть кількість"),
            NumberRange(min=0, message="Кількість не може бути від'ємною")
        ]
    )

    image = FileField(
    "Зображення товару",
    validators=[
        FileAllowed(["jpg", "jpeg", "png"], "Дозволені лише JPG, JPEG та PNG!"),
        FileSize(max_size=2 * 1024 * 1024, message="Максимальний розмір зображення — 2 МБ!")
    ]
)

    submit = SubmitField("Зберегти товар")
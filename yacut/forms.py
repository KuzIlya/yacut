from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional

from .constants import MIN_SHORT_LENGTH, MAX_SHORT_LENGTH


class URLForm(FlaskForm):
    original_link = URLField(
        "Длинная ссылка",
        validators=[
            DataRequired(message="Обязательное поле"),
            URL(message="Некорректный URL"),
        ],
    )
    custom_id = StringField(
        "Ваш вариант короткой ссылки",
        validators=[
            Optional(),
            Length(
                MIN_SHORT_LENGTH,
                MAX_SHORT_LENGTH,
                message=(
                    "Длина вашего идентификатора дожна "
                    "быть от 1 до 16 символов"
                ),
            ),
        ],
    )
    submit = SubmitField("Создать")

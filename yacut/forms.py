from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional


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
                1,
                16,
                message=(
                    "Длина вашего идентификатора дожна " "быть от 1 до 16 символов"
                ),
            ),
        ],
    )
    submit = SubmitField("Создать")

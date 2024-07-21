from http import HTTPStatus
from string import ascii_letters, digits

from flask import jsonify, request
from validators import url

from . import app, db
from .constants import MIN_SHORT_LENGTH, MAX_SHORT_LENGTH
from .errors_handlers import InvalidAPIUsage, UniquenessError
from .models import URLMap
from .utils import get_unique_short_id


@app.route("/api/id/", methods=["POST"])
def create_short_id():
    global counter
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса")
    if "url" not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if not url(data["url"]):
        raise InvalidAPIUsage("Длинная ссылка не работает")
    if "custom_id" in data and data["custom_id"]:
        if URLMap.query.filter_by(short=data["custom_id"]).first():
            raise InvalidAPIUsage(
                "Предложенный вариант короткой ссылки уже существует."
            )
        if not (
            MIN_SHORT_LENGTH <= len(data["custom_id"]) <= MAX_SHORT_LENGTH
            and all(
                char in ascii_letters + digits for char in data["custom_id"]
            )
        ):
            raise InvalidAPIUsage(
                "Указано недопустимое имя для короткой ссылки"
            )
    else:
        try:
            data["custom_id"] = get_unique_short_id()
        except UniquenessError:
            raise InvalidAPIUsage(
                "Ошибка со стороны сервера",
                HTTPStatus.INTERNAL_SERVER_ERROR
            )

    url_map = URLMap(original=data["url"], short=data["custom_id"])
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_original_link(short_id):
    if not (url_map := URLMap.query.filter_by(short=short_id).first()):
        raise InvalidAPIUsage("Указанный id не найден", HTTPStatus.NOT_FOUND)
    return jsonify({"url": url_map.original}), HTTPStatus.OK

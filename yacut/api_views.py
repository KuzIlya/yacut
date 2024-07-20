from string import ascii_letters, digits

from flask import jsonify, request

from . import app, db
from .errors_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route("/api/id/", methods=["POST"])
def create_short_id():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса")
    if "url" not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if "custom_id" in data and data["custom_id"]:
        if URLMap.query.filter_by(short=data["custom_id"]).first():
            raise InvalidAPIUsage(
                "Предложенный вариант короткой " "ссылки уже существует."
            )
        if not (
            1 <= len(data["custom_id"]) <= 16
            and all(letter in ascii_letters + digits for letter in data["custom_id"])
        ):
            raise InvalidAPIUsage("Указано недопустимое " "имя для короткой ссылки")
    else:
        while True:
            generated_short = get_unique_short_id()
            if not URLMap.query.filter_by(short=generated_short).first():
                data["custom_id"] = generated_short
                break

    url_map = URLMap(original=data["url"], short=data["custom_id"])
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_original_link(short_id):
    if not (url_map := URLMap.query.filter_by(short=short_id).first()):
        raise InvalidAPIUsage("Указанный id не найден", 404)
    return jsonify({"url": url_map.original}), 200

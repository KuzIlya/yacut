from flask import abort, flash, redirect, render_template, request

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id
from .errors_handlers import UniquenessError


@app.route("/", methods=["GET", "POST"])
def index_page():
    form = URLForm()
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data
        if short and URLMap.query.filter_by(short=short).first():
            flash(
                "Предложенный вариант короткой ссылки уже существует.",
                "Warninig",
            )
            return render_template("index.html", form=form)
        if not short:
            try:
                short = get_unique_short_id()
            except UniquenessError:
                abort(500)

        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        flash(request.host_url + url_map.short, "Success")
    return render_template("index.html", form=form)


@app.route("/<string:short>")
def redirect_to_original_link(short):
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original)

import click

from . import app, db
from .models import URLMap
from .utils import MAX_COMBINES, get_unique_short_id


@app.cli.command("delete_links")
def delete_all_links_command():
    """Функция удаления всех ссылок из базы данных"""
    objects = URLMap.query.all()
    deleted_links = 0

    for obj in objects:
        db.session.delete(obj)
        db.session.commit()
        deleted_links += 1

    click.echo(f"Удалено записей: {deleted_links}")


@app.cli.command("delete_link")
@click.argument("id")
def delete_link(id):
    """Функция удаления объекта по id"""
    id = int(id)
    link = URLMap.query.get(id)
    if link:
        db.session.delete(link)
        db.session.commit()
        click.echo(f"Объект с {id=} был удален")
    else:
        click.echo(f"Объект с {id=} не существует")


@app.cli.command("check_short_counter")
def check_short_counter_command():
    """Проверить количество доступных имен"""
    current_combines = get_unique_short_id.counter()
    click.echo(f"Количество свободных имен: {MAX_COMBINES - current_combines}")

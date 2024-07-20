from . import app, db


@app.route('/api/id/', methods=['POST'])
def create_short_id():
    pass


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short_id):
    pass
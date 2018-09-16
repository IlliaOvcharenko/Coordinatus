from flask import *
from modules.Point import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/build_join', methods=['GET', 'POST'])
def build_join():
    print('EXECUTE: build_join()')
    if request.is_json:
        points = request.get_json()
        return jsonify(points_to_dict(dict_to_points(points)))
    return abort(400)


if __name__ == '__main__':
    app.run()

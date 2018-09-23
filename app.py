from flask import *
from modules.Point import *
from modules.ConvexHull import *
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/build_convex_hull', methods=['GET', 'POST'])
def build_convex_hull():
    print('EXECUTE: build_convex_hull()')
    if request.is_json:
        points_dict = request.get_json()
        points = dict_to_points(points_dict)
        start_time = time.monotonic()
        convex_hull = graham_scan(points)
        end_time = time.monotonic()

        response = {
            'convex_hull': points_to_dict(convex_hull),
            'execution_time': end_time - start_time
        }
        return jsonify(response)
    return abort(400)


if __name__ == '__main__':
    app.run()

from flask import Flask, g
import os
import markdown
import shelve
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("devices.db")
    return db

@app.teardown_appcontect
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    """Some Documentation"""

    # Open the ReadMe File
    with open(os.path.dirname(app.root_path) + '/ReadMe.md', 'r' ) as markdown_file:
        content = markdown_file.read()

        return markdown.markdown(content)


class DeviceList(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        devices = []

        for key in keys:
            devices.append(shelf[key])

        return {'message': 'Success', 'data' : devices}
        
    def post(self):
        parser = reqparse.ReuestParser()

        parser.add_argument('identifier', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('device_type', required=True)
        parser.add_argument('controller_gateway', required=True)

        args = parser.parse_args()

        shelf = get_db()
        shelf[args['identifier']] = args

        return {'message': 'Device Registered', 'data':args}, 201

class Device(Resource):
    def get(shelf,identifier):
        shelf = get_db()
        if not (identifier in shelf):
            return {'message': 'Device not Found', 'data':{}}, 404

        return {'message': 'Device Found', 'data':shelf[identifier]}, 200

    def delete(shelf,identifier):
        shelf = get_db()
        if not (identifier in shelf):
            return {'message': 'Device not Found', 'data':{}}, 404

        del shelf[identifier]
        return '',204
        

api.add_resource(DeviceList,'/devices')
api.add_resource(Device, '/device/<string:identifier>')
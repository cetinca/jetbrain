from flask import Flask, abort
import sys
from flask_restful import Api
from db import db
from event_resource import EventResource, TodayResource, IdResource

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event.db'


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(404)
def not_found():
    abort(404)


api.add_resource(EventResource, "/event")
api.add_resource(TodayResource, "/event/today")
api.add_resource(IdResource, "/event/<_id>")

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        db.init_app(app)
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        db.init_app(app)
        app.run()

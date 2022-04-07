import os
import sys
from db import db
from city_view import city_blueprint
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, render_template
from time import strftime
import traceback

app = Flask(__name__)
app.config.from_object('settings')
key = os.urandom(24)  # specify the length in brackets
app.config['SECRET_KEY'] = key

app.register_blueprint(city_blueprint)


def init():
    app.handler = RotatingFileHandler('.app.log', maxBytes=100000, backupCount=3)
    app.logger = logging.getLogger('tdm')
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(app.handler)
    db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    app.logger.info('%s %s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme,
                    request.full_path,
                    response.status,
                    request.values
                    )
    return response


@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    app.logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr, request.method,
                     request.scheme, request.full_path, tb)
    return e.status_code


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", error=e)


@app.errorhandler(500)
def not_found2(e):
    return render_template("error.html", error=e)


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        init()
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)

    else:
        init()
        db.init_app(app)
        app.run()

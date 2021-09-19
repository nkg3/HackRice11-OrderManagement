import os

from flask import Flask, render_template
from . import worker, dashboard, database
from .notifier import Notifier

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/")
    def hello():
        return render_template('base.html')

    @app.context_processor
    def get_work_orders():
        return dict(work_orders=database.get_under_directory('/WorkOrders'))

    @app.context_processor
    def db_processor():
        def get_workers():
            return database.get_under_directory('/Workers')
        def get_facilities():
            return database.get_under_directory('/Facilities')
        def get_work_orders():
            return database.get_under_directory('/WorkOrders')
        def get_equipments():
            return database.get_under_directory('/Equipments')
        return dict(get_workers=get_workers, get_facilities=get_facilities, get_work_orders=get_work_orders, get_equipments=get_equipments)

    database.init_database('https://hackrice11-ordermanageme-327b0-default-rtdb.firebaseio.com/', './DataFiles/database_private_key.json')

    app.register_blueprint(worker.bp)
    app.register_blueprint(dashboard.bp)

    return app
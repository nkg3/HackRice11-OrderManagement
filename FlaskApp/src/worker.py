import functools
from . import database as db
from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

orders = {}

bp = Blueprint('worker', __name__, url_prefix='/worker')

@bp.route("/")
def hello():
    return render_template('worker/worker.html')

@bp.route("/<int:id>/delete", methods = ('POST',))
def finish(id):
    order = db.get_under_directory('/WorkOrders/'+str(id))
    order['done'] = "True"
    order['inProgress'] = "False"
    order['Completion Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.update('/WorkOrders/'+str(id), order)
    return redirect(url_for('worker.hello'))
import functools
from . import database as db
from . import scheduler
from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

orders = {}

bp = Blueprint('worker', __name__, url_prefix='/worker')

@bp.route("/<Name>")
def hello(Name):
    return render_template('worker/worker.html', name=Name)

@bp.route("/<Name>/<int:id>/delete", methods = ('POST',))
def finish(id, Name):
    order = db.get_under_directory('/WorkOrders/'+str(id))
    order['done'] = "True"
    order['inProgress'] = "True"
    order['Completion Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.update('/WorkOrders/'+str(id), order)
    worker = db.get_under_directory('/Workers/'+str(order['Assigned']))
    worker['inTask'] = 'False'
    worker['assigned'] = 'None'
    worker['TasktimeLeft'] = '0'
    db.update('/Workers/'+str(order['Assigned']), worker)

    if datetime.now().hour >= 12:
        scheduler.updateWholeThing('Evening')
    else:
        scheduler.updateWholeThing('Morning')
    return redirect(url_for('worker.hello', Name=Name))
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

orders = {}

bp = Blueprint('worker', __name__, url_prefix='/worker')

@bp.route("/")
def hello():
    return render_template('worker/worker.html', orders=orders)

@bp.route("/<int:id>/delete", methods = ('POST',))
def finish(id):
    for order in orders:
        if orders[order]['order no.'] == str(id):
            orders[order]['finished'] = True
            print('Finished!')
    return redirect(url_for('worker.hello'))

def create_orders():
    orders[0] = {
        "order no." : "1001",
        "name" : "Joe",
        "equipment" : "electrical",
        "facility" : "fac4",
        "priority" : "5",
        "time" : "3:00:00",
        "finished" : False
    }
    orders[1] = {
        "order no." : "1002",
        "name" : "Jill",
        "equipment" : "electricals",
        "facility" : "fac5",
        "priority" : "3",
        "time" : "4:00:00",
        "finished" : False
    }
    orders[2] = {
        "order no." : "1003",
        "name" : "Jill",
        "equipment" : "electricals",
        "facility" : "fac5",
        "priority" : "3",
        "time" : "4:00:00",
        "finished" : False
    }

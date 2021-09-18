import functools
from . import database as db

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
    db.update
    return redirect(url_for('worker.hello'))
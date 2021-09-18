import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('dash', __name__, url_prefix='/dashboard')

@bp.route("/")
def hello():
    return render_template('dashboard/dashboard.html')
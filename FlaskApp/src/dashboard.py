import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('dash', __name__, url_prefix='/dashboard')

# Dashboard home
@bp.route("/")
def home():
    return render_template('dashboard/dashboard.html')

# Add new work order
@bp.route("/addOrder")
def add_order():
    return render_template('dashboard/orderform.html')

# Monitor Routes
@bp.route("/orders")
def orders():
    return render_template('dashboard/orders.html')

@bp.route("/workers")
def workers():
    return render_template('dashboard/workers.html')

@bp.route("/facilities")
def facilities():
    return render_template('dashboard/facilities.html')

@bp.route("/equipment")
def equipment():
    return render_template('dashboard/equipment.html')
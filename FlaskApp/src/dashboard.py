import functools
import os

from . import database as db
from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'xlsx', 'txt', 'jpg'}
UPLOAD_FOLDER = './Uploads'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

bp = Blueprint('dash', __name__, url_prefix='/dashboard')

# Dashboard home
@bp.route("/")
def home():
    return render_template('dashboard/dashboard.html')

# Add new work order
@bp.route("/addOrder", methods=('GET','POST'))
def add_order():
    if(request.method == 'POST'):
        facility = request.form['facility']
        eq_type = request.form['type']
        eq_ID = request.form['equipment-id']
        priority = request.form['inlineRadioOptions']
        complete_time = request.form['complete_time']
        error = None

        if not facility:
            error = 'Please select a facility.'
        elif not eq_type:
            error = 'Please select an equipment type.'
        elif not eq_ID:
            error = 'Please input a valid ID'
        elif not priority:
            error = 'Please select a priority'
        elif not complete_time:
            error = 'Please enter an estimated completion time'

        order_id = str(int(max(db.get_under_directory('/WorkOrders').keys()))+1)

        new_order={
                    'Equipment ID' : eq_ID,
                    'Equipment Type': eq_type,
                    'Facility' : facility,
                    'Priority(1-5)': priority,
                    'Submission Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'Time to Complete': complete_time,
                    'Work Order ': order_id,
                    'done' : 'False',
                    'inProgress' : 'False',
                    'newPrior': 'None',
                    'timeLeft': '0'
                }

        if error is None:
            #try:
                db.update('/WorkOrders/'+order_id, new_order)
            #except:
            #    error = 'Something went wrong! Try again later'

        flash(error)

    return render_template('dashboard/orderform.html')

#Upload XLSX
@bp.route("/addOrder/upload", methods=('GET','POST'))
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('dash.add_order'))
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('dash.add_order'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('dash.add_order'))
    
    return redirect(url_for('dash.add_order'))


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
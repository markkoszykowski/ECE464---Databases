from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import is_admin
from .db_config import workoutsDB

main = Blueprint('main', __name__)

@main.route('/')
def index():
	if current_user.is_authenticated:
		admin = is_admin(current_user.id)
	else:
		admin = False
	return render_template('index.html', admin=admin)

@main.route('/profile')
@login_required
def profile():
	user = workoutsDB.db.tracker.find_one({"_id": current_user.id})
	try:
		history = reversed(user['history'])
	except:
		history = None
	return render_template('profile.html', name=current_user.name, admin=is_admin(current_user.id), user=user, history=history)

@main.route('/profile', methods=['POST'])
@login_required
def track():
	try:
		weight = int(request.form.get('weight')) if request.form.get('weight') else None
	except:
		flash("Please enter valid a resposne")
		return redirect(url_for('main.profile'))

	if weight is None or weight <= 0:
		flash("Please enter a valid weight")
		return redirect(url_for('main.profile'))

	entry = workoutsDB.db.tracker.find_one({"_id": current_user.id,
											"history.date": datetime.today().strftime('%m-%d-%Y')})

	if entry:
		flash("Can only log one weigh-in/workout per day")
		return redirect(url_for('main.profile'))

	workoutsDB.db.tracker.update({"_id": current_user.id},
								 {"$push":
									 {"history":
										 {"date": datetime.today().strftime('%m-%d-%Y'),
											 "weight": weight
										 }
									 }
								 })
	return redirect(url_for('main.profile'))
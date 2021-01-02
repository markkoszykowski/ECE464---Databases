from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .db_config import usersDB, workoutsDB
from .models import User, Role, UserRoles

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
	return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
	email = request.form.get('email')
	password = request.form.get('password')
	remember = True if request.form.get('remember') else False

	user = User.query.filter_by(email=email).first()

	if not user or not check_password_hash(user.password, password):
		flash('Login was not correct')
		return redirect(url_for('auth.login'))

	login_user(user, remember=remember)
	return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
	return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
	email = request.form.get('email') if request.form.get('email') else None
	name = request.form.get('name') if request.form.get('name') else None
	password = request.form.get('password') if request.form.get('password') else None
	sex = request.form.get('sex').lower() if request.form.get('sex') else None
	DOB = request.form.get('DOB') if request.form.get('DOB') else None
	try:
		height = float(request.form.get('height')) if request.form.get('height') else None
	except:
		flash('Please enter a valid height')
		return redirect(url_for('auth.signup'))

	if not email or not name or not password or not sex or not height or not DOB:
		flash('Please enter the following information')
		return redirect(url_for('auth.signup'))

	if height <= 0:
		flash('Please enter a valid height')
		return redirect(url_for('auth.signup'))

	if sex != 'm' and sex != 'f':
		flash('Please enter a valid sex')
		return redirect(url_for('auth.signup'))

	age = (datetime.today() - datetime.strptime(DOB, '%Y-%m-%d')).days / 365

	if age < 13:
		flash('Must be 13 years or older to use this service')
		return redirect(url_for('auth.signup'))

	user = User.query.filter_by(email=email).first()

	if user:
		flash('Email Address already exists, please login')
		return redirect(url_for('auth.signup'))
	hashed_pass = generate_password_hash(password, method='sha256')

	DOB = datetime.strftime(datetime.strptime(DOB, '%Y-%m-%d'), '%m-%d-%Y')

	new_user = User(email=email, name=name, password=hashed_pass)
	assigned_role = Role.query.filter_by(name='user').first()
	new_user.roles.append(assigned_role)
	usersDB.session.add(new_user)
	usersDB.session.commit()

	workoutsDB.db.tracker.insert_one({"_id": new_user.id, "sex": sex, "height": height, "DOB": DOB})
	return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.index'))

@auth.route('/addadmin', methods=['POST'])
@login_required
def add_admin():
	email = request.form.get('new_admin') if request.form.get('new_admin') else None
	if not email:
		flash("Please enter a valid email")
		return redirect(url_for('main.profile'))

	user = User.query.filter_by(email=email).first()

	if not user:
		flash("Please enter an email account that exists")
		return redirect(url_for('main.profile'))

	userrole = UserRoles.query.filter_by(user_id=user.id).first()
	userrole.role_id = 0
	usersDB.session.commit()

	flash(F"User {email} switched to admin")
	return redirect(url_for('main.profile'))
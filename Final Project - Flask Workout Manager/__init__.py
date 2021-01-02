from flask import Flask
from .db_config import usersDB, workoutsDB
from .log import login_manager
from .models import User, Role
from werkzeug.security import generate_password_hash

def create_app():
	app = Flask(__name__)

	app.config['SECRET_KEY'] = 'supersecretkey'
	app.config['MONGO_URI'] = 'mongodb://localhost:27017/workoutManager'
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

	workoutsDB.init_app(app)
	usersDB.init_app(app)
	login_manager.init_app(app)

	with app.app_context():
		usersDB.create_all()
		if not Role.query.filter_by().first():
			usersDB.session.add(Role(id=0, name='admin'))
			usersDB.session.add(Role(id=1, name='user'))

			admin = User(email='mkoszy@cooper.edu', name='Mark',
				 password=generate_password_hash("password", method='sha256'))
			admin.roles.append(Role.query.filter_by(name='admin').first())

			usersDB.session.add(admin)
			usersDB.session.commit()

			workoutsDB.db.tracker.delete_many({})
			workoutsDB.db.tracker.insert_one({"_id": admin.id, "sex": 'm', "height": 6, "DOB": "05-25-2000"})
			workoutsDB.db.workouts.create_index([( "$**", "text" )])


	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .work import work as work_blueprint
	app.register_blueprint(work_blueprint)

	return app
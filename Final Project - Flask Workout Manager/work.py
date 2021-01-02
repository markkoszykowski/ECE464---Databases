import re
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .db_config import workoutsDB
from .models import is_admin

work = Blueprint('work', __name__)

@work.route('/search', methods=['POST'])
@login_required
def search():
    s = request.form.get('search') if request.form.get('search') else None
    if not s:
        return redirect(url_for('work.workouts', sort='name', scend=1))

    search = s.lower()
    results = workoutsDB.db.workouts.find({"$text": {"$search": search}})
    if results.count() == 0:
        results = None
    return render_template("search.html", search=s, results=results, admin=is_admin(current_user.id))

@work.route('/add')
@login_required
def add():
    exercises = workoutsDB.db.exercises.find({}).sort("name")
    return render_template('exercises.html', exercises=exercises, admin=is_admin(current_user.id))

@work.route('/add', methods=['POST'])
@login_required
def add_post():
    exercise_name = request.form.get('exercise').lower() if request.form.get('exercise') else None
    exercise_note = request.form.get('notes') if request.form.get('notes') else None

    if not exercise_name:
        flash('Please enter exercise name')
        return redirect(url_for('work.add'))

    id = re.sub(r'\W+', '', exercise_name)

    exercise = workoutsDB.db.exercises.find_one({"_id": str(id)})
    if exercise:
        flash('Exercise already exists')
        return redirect(url_for('work.add'))

    if exercise_note:
        workoutsDB.db.exercises.insert_one({"_id": str(id), "name": exercise_name, "notes": exercise_note})
    else:
        workoutsDB.db.exercises.insert_one({"_id": str(id), "name": exercise_name})
    return redirect(url_for('work.add'))

@work.route('/delete/<exercise_name>')
@login_required
def delete(exercise_name):
    id = re.sub(r'\W+', '', exercise_name)
    workoutsDB.db.workouts.update({}, {"$pull": {"exercises": {"name": exercise_name}}}, multi=True)
    workoutsDB.db.exercises.delete_one({"_id": str(id)})
    return redirect(url_for('work.add'))

@work.route('/create')
@login_required
def create():
    workouts = workoutsDB.db.workouts.find({}).sort("name")
    return render_template('create_workout.html', workouts=workouts, admin=is_admin(current_user.id))

@work.route('/create', methods=['POST'])
@login_required
def create_post():
    workout_name = request.form.get('workout').lower() if request.form.get('workout') else None
    try:
        difficulty = int(request.form.get('difficulty')) if request.form.get('difficulty') else None
        length = float(request.form.get('length')) if request.form.get('length') else None
    except:
        flash('Please enter information in the correct format')
        return redirect(url_for('work.create'))

    if not workout_name:
        flash('Please enter workout name')
        return redirect(url_for('work.create'))

    if not difficulty:
        flash('Please enter difficulty level')
        return redirect(url_for('work.create'))

    if not length:
        flash('Please enter length of workout')
        return redirect(url_for('work.create'))

    if difficulty > 3 or difficulty < 1:
        flash('Please enter a valid difficulty')
        return redirect(url_for('work.create'))

    if length <= 0:
        flash('Please enter a valid length')
        return redirect(url_for('work.create'))


    id = re.sub(r'\W+', '', workout_name)

    workout = workoutsDB.db.workouts.find_one({"_id": str(id)})
    if workout:
        flash('Workout already exists')
        return redirect(url_for('work.create'))

    workoutsDB.db.workouts.insert_one({"_id": str(id), "name": workout_name, "diff": difficulty, "length": length, "uses": 0})
    return redirect(url_for('work.append', workout_name=workout_name))

@work.route('/append/<workout_name>')
@login_required
def append(workout_name):
    id = re.sub(r'\W+', '', workout_name)
    workout_exercises = workoutsDB.db.workouts.find_one({"_id": str(id)})
    exercises = workoutsDB.db.exercises.find({}).sort("name")
    return render_template("edit_workout.html", workout_name=workout_name, workout_exercises=workout_exercises, exercises=exercises, admin=is_admin(current_user.id))

@work.route('/append/<workout_name>/<exercise_name>', methods=['POST'])
@login_required
def append_post(workout_name, exercise_name):
    try:
        order = int(request.form.get('order')) - 1 if request.form.get('order') else None
        weight = float(request.form.get('weight')) if request.form.get('weight') else None
        reps = int(request.form.get('reps')) if request.form.get('reps') else None
        sets = int(request.form.get('sets')) if request.form.get('sets') else None
        time = float(request.form.get('time')) if request.form.get('time') else None
    except:
        flash("Please enter (a) valid response(s)")
        return redirect(url_for('work.append', workout_name=workout_name))

    id = re.sub(r'\W+', '', workout_name.lower())

    workouts = workoutsDB.db.workouts.aggregate([
        {"$match": {"_id": str(id)}},
        {"$project":
             {"size":
                  {"$size":
                       {"$ifNull" : ["$exercises", []]}
                   }
              }
        }
    ])
    length = 0
    for workout in workouts:
        length = workout['size']

    if order is None or order < 0:
        flash('Please enter a valid order')
        return redirect(url_for('work.append', workout_name=workout_name))
    if order > length:
        flash(F'Workout only has {length} exercises right now')
        return redirect(url_for('work.append', workout_name=workout_name))

    workoutsDB.db.workouts.update({"_id": str(id)},
                                  {"$push":
                                      {"exercises":
                                          {"$each": [{
                                              "name": exercise_name,
                                              "weight": weight,
                                              "reps": reps,
                                              "sets": sets,
                                              "time": time
                                          }],
                                              "$position": order}
                                      }
                                  })
    return redirect(url_for('work.append', workout_name=workout_name))

@work.route('/remove/<workout_name>')
@login_required
def remove(workout_name):
    id = re.sub(r'\W+', '', workout_name)
    workoutsDB.db.workouts.delete_one({"_id": str(id)})
    return redirect(url_for('work.create'))

@work.route('/pop/<workout_name>/<index>')
@login_required
def pop(workout_name, index):
    index = int(index) - 1
    filt = F"exercises.{index}"

    id = re.sub(r'\W+', '', workout_name.lower())

    workoutsDB.db.workouts.update_one({"_id": str(id)},
                                      {"$unset":
                                           {filt: 1}})
    workoutsDB.db.workouts.update_one({"_id": str(id)},
                                      {"$pull":
                                           {"exercises": None}})
    return redirect(url_for('work.append', workout_name=workout_name))

@work.route('/exe/<exercise_name>')
@login_required
def exercise(exercise_name):
    id = re.sub(r'\W+', '', exercise_name)
    exercise = workoutsDB.db.exercises.find_one({"_id": str(id)})
    return render_template('exercise.html', exercise=exercise, admin=is_admin(current_user.id))

@work.route('/wor/<workout_name>')
@login_required
def workout(workout_name):
    id = re.sub(r'\W+', '', workout_name)
    workout = workoutsDB.db.workouts.find_one({"_id": str(id)})
    return render_template('workout.html', workout=workout, admin=is_admin(current_user.id))

@work.route('/workouts/<sort>/<scend>')
@login_required
def workouts(sort, scend):
    workouts = workoutsDB.db.workouts.find({}).sort([(sort, int(scend))])
    return render_template('workouts.html', workouts=workouts, admin=is_admin(current_user.id))

@work.route('/track/<workout_name>', methods=['POST'])
@login_required
def track(workout_name):
    try:
        weight = int(request.form.get('weight')) if request.form.get('weight') else None
    except:
        flash("Please enter a valid response")
        return redirect(url_for('work.workouts', sort='name', scend=1))

    entry = workoutsDB.db.tracker.find_one({"_id": current_user.id,
                                            "history.date": datetime.today().strftime('%m-%d-%Y')})


    if entry:
        flash("Can only log one weigh-in/workout per day")
        return redirect(url_for('work.workouts', sort='name', scend=1))

    if weight and weight > 0:
        workoutsDB.db.tracker.update({"_id": current_user.id},
                                    {"$push":
                                         {"history":
                                             {"date": datetime.today().strftime('%m-%d-%Y'),
                                             "weight": weight,
                                             "workout": workout_name
                                             }
                                         }
                                    })
    else:
        workoutsDB.db.tracker.update({"_id": current_user.id},
                                     {"$push":
                                         {"history":
                                             {"date": datetime.today().strftime('%m-%d-%Y'),
                                             "workout": workout_name
                                             }
                                         }
                                     })

    id = re.sub(r'\W+', '', workout_name.lower())

    workoutsDB.db.workouts.update({"_id": str(id)},
                                  {"$inc": {"uses": 1}})

    return redirect(url_for('work.workouts', sort='name', scend=1))

@work.route('/progress')
@login_required
def progress():
	user = workoutsDB.db.tracker.find_one({'_id': current_user.id})

	return render_template('progress.html',  admin=is_admin(current_user.id), user=user)

@work.route('/stats')
@login_required
def stats():
    workouts = workoutsDB.db.workouts.find({})
    temp = []
    for wo in workouts:
        temp.append(wo)
    return render_template('stats.html', admin=is_admin(current_user.id), workouts=temp)
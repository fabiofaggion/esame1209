from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import user_dao
import workout_dao  
from models import User

###############################
#########TODO QUESTO CODICE è DA IMPLEMENTARE?
###############################
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# # Importa i modelli
# from models import User, Trainer, Client, Workout, TrainingPlan


# Create the application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'trisetitri'

login_manager = LoginManager()
login_manager.init_app(app)

# Error Handler
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# CLIENT ROUTE SECTION
@app.route('/home_client')
@login_required
def home_client():
    trainers = get_all_trainers()  # Funzione che recupera tutti i personal trainer dal database
    return render_template('client/home_client.html', trainers=trainers)

@app.route('/choose_trainer')
@login_required
def choose_trainer():
    trainers = Trainer.query.all() # TODO CAMBIARE NOME VARIABILE
    return render_template('choose_trainer.html', trainers=trainers)

@app.route('/profile_client')
@login_required
def profile_client():
    return render_template('client/profile_client.html')

# PERSONAL ROUTE SECTION
@app.route('/home_personal')
@login_required
def home_personal():
    public_workouts = get_public_workouts()  # Funzione che recupera allenamenti pubblici
    private_workouts = get_private_workouts()  # Funzione che recupera allenamenti privati
    return render_template('home_personal.html', public_workouts=public_workouts, private_workouts=private_workouts)    

@app.route('/profile_personal')
def profile_personal():
    return render_template('personal/profile_personal.html')

@app.route('/create_training_plan')
def create_training_plan():
    return render_template('personal/create_training_plan.html')

@app.route('/edit_training_plan')
def edit_training_plan():
    return render_template('personal/edit_training_plan.html')

@app.route('/delete_training_plan')
def delete_training_plan():
    return render_template('personal/delete_training_plan.html')

@app.route('/view_training_plan')
def view_training_plan():
    return render_template('personal/view_training_plan.html')

@app.route('/create_workout')
def create_workout():
    return render_template('personal/create_workout.html')

@app.route('/edit_workout')
def edit_workout():
    return render_template('personal/edit_workout.html')

@app.route('/delete_workout')
def delete_workout():
    return render_template('personal/delete_workout.html')

# Route BASE
@app.route('/base')
def base():
    return render_template('base.html')

# Route SIGNUP 
@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Extract form data into a dictionary
        new_user_from_form = request.form.to_dict()
        
        # Check if user already exists in the database
        user_in_db = user_dao.get_user_by_username(new_user_from_form.get('username'))
        if user_in_db:
            flash('C\'è già un utente registrato con questo nickname', 'danger')
            return redirect(url_for('sign_up'))

        # Hash the user's password
        new_user_from_form['password'] = generate_password_hash(new_user_from_form.get('password'))
        
        # Capture user type from the form
        new_user_from_form['user_type'] = new_user_from_form.get('user_type')

        # Save the new user in the database
        success = user_dao.create_user(new_user_from_form)

        if success:
            flash('New profile created', 'success')
            return redirect(url_for('base'))
        else:
            flash('Errore nella creazione del utente: riprova!', 'danger')
            return redirect(url_for('sign_up'))
    return render_template('signup.html')

# Route LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Logica di autenticazione
        user_in_db = user_dao.get_user_by_username(username)
        if user_in_db and check_password_hash(user_in_db['password'], password):
            user = User(id=user_in_db['id'], username=user_in_db['username'], password=user_in_db['password'], type=user_in_db['user_type'])
            login_user(user)
            flash('Login successful', 'success')
            if user.type == 'personal_trainer':
                return redirect(url_for('home_personal'))
            else:
                return redirect(url_for('home_client'))
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

# LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Questo è fornito da Flask-Login per effettuare il logout
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    db_user = user_dao.get_user_by_id(user_id)
    if db_user:
        return User(id=db_user['id'], username=db_user['username'], password=db_user['password'], type=db_user['user_type'])
    return None

if __name__ == '__main__':
    app.run(debug=True)


#############################################
############# TODO ROUTE TESTING ############
#############################################

# Rotta per visualizzare il profilo del cliente
# @app.route('/profile_client')
# def profile_client():
#     if 'client_id' not in session:
#         flash('Please log in first.')
#         return redirect(url_for('login'))

#     client_id = session['client_id']
#     client = Client.query.get(client_id)
#     trainer = client.trainer  # Associazione uno a uno tra Cliente e Trainer
#     training_plans = TrainingPlan.query.filter_by(client_id=client_id).all()

#     return render_template('profile_client.html', client=client, training_plans=training_plans)

################################################

# Rotta per valutare una scheda di allenamento
# @app.route('/rate_plan/<int:plan_id>', methods=['POST'])
# def rate_plan(plan_id):
#     if 'client_id' not in session:
#         flash('Please log in first.')
#         return redirect(url_for('login'))

#     rating = int(request.form['rating'])
#     training_plan = TrainingPlan.query.get(plan_id)
#     if not training_plan or training_plan.client_id != session['client_id']:
#         flash('Invalid request.')
#         return redirect(url_for('profile_client'))

#     # Aggiorna la valutazione della scheda
#     training_plan.rating = rating
#     db.session.commit()

#     # Calcola il nuovo rating del personal trainer
#     trainer = training_plan.trainer
#     all_ratings = [plan.rating for plan in trainer.training_plans if plan.rating is not None]
#     trainer.rating = sum(all_ratings) / len(all_ratings) if all_ratings else 0
#     db.session.commit()

#     flash('Rating submitted successfully.')
#     return redirect(url_for('profile_client'))

########################################################

# # Rotta per la home del personal trainer
# @app.route('/home_personal')
# def home_personal():
#     if 'trainer_id' not in session:
#         flash('Please log in first.')
#         return redirect(url_for('login'))
    
#     trainer_id = session['trainer_id']
#     trainer = Trainer.query.get(trainer_id)
#     public_workouts = Workout.query.filter_by(is_public=True).order_by(Workout.created_at.desc()).all()
#     return render_template('home_personal.html', trainer=trainer, public_workouts=public_workouts)

# # Rotta per creare un nuovo allenamento
# @app.route('/create_workout', methods=['GET', 'POST'])
# def create_workout():
#     if 'trainer_id' not in session:
#         flash('Please log in first.')
#         return redirect(url_for('login'))
    
#     if request.method == 'POST':
#         title = request.form['title']
#         description = request.form['description']
#         level = request.form['level']
#         is_public = 'is_public' in request.form
#         trainer_id = session['trainer_id']
        
#         new_workout = Workout(title=title, description=description, level=level, is_public=is_public, trainer_id=trainer_id)
#         db.session.add(new_workout)
#         db.session.commit()
#         flash('Workout created successfully!')
#         return redirect(url_for('home_personal'))
    
#     return render_template('create_workout.html')

# # Rotta per modificare un allenamento
# @app.route('/edit_workout/<int:workout_id>', methods=['GET', 'POST'])
# def edit_workout(workout_id):
#     workout = Workout.query.get_or_404(workout_id)
#     if 'trainer_id' not in session or workout.trainer_id != session['trainer_id']:
#         flash('Unauthorized action.')
#         return redirect(url_for('home_personal'))
    
#     if request.method == 'POST':
#         workout.title = request.form['title']
#         workout.description = request.form['description']
#         workout.level = request.form['level']
#         workout.is_public = 'is_public' in request.form
#         db.session.commit()
#         flash('Workout updated successfully!')
#         return redirect(url_for('home_personal'))
    
#     return render_template('edit_workout.html', workout=workout)

# # Rotta per eliminare un allenamento
# @app.route('/delete_workout/<int:workout_id>', methods=['POST'])
# def delete_workout(workout_id):
#     workout = Workout.query.get_or_404(workout_id)
#     if 'trainer_id' not in session or workout.trainer_id != session['trainer_id']:
#         flash('Unauthorized action.')
#         return redirect(url_for('home_personal'))
    
#     db.session.delete(workout)
#     db.session.commit()
#     flash('Workout deleted successfully!')
#     return redirect(url_for('home_personal'))

##############################################

# # Rotta per la pagina del profilo del personal trainer
# @app.route('/profile_personal')
# def profile_personal():
#     if 'trainer_id' not in session:
#         flash('Please log in first.')
#         return redirect(url_for('login'))
    
#     trainer_id = session['trainer_id']
#     trainer = Trainer.query.get(trainer_id)
    
#     # Calcolare il rating medio
#     if trainer.training_plans:
#         total_rating = sum(plan.rating for plan in trainer.training_plans if plan.rating is not None)
#         count = sum(1 for plan in trainer.training_plans if plan.rating is not None)
#         trainer.rating = total_rating / count if count > 0 else 0
    
#     public_workouts = [workout for workout in trainer.workouts if workout.is_public]
#     private_workouts = [workout for workout in trainer.workouts if not workout.is_public]
    
#     return render_template('profile_personal.html', trainer=trainer, public_workouts=public_workouts, private_workouts=private_workouts)

# # Rotta di login (placeholder per contesto)
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     # Implementa la logica di login qui
#     return 'Login placeholder'

# # Rotta per logout
# @app.route('/logout')
# def logout():
#     session.pop('trainer_id', None)
#     flash('You have been logged out.')
#     return redirect(url_for('login'))
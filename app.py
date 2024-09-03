from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import user_dao
import workout_dao  
from models import User

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
def choose_trainer():
    return render_template('client/choose_trainer.html')

@app.route('/profile_client')
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

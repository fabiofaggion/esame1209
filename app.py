from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import user_dao
import clients_dao
import personal_trainers_dao
import workouts_dao
import workout_sheets_dao
import worksheet_rating_dao
import personal_trainers_dao
from models import User

# Crea l'applicazione
app = Flask(__name__)
app.config['SECRET_KEY'] = 'trisetitri'

# Configura Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Funzione per testare la connessione al database
def test_db_connection():
    try:
        # Usa il percorso corretto al database
        connection = sqlite3.connect('C:/Users/Fabio/Desktop/flask/esame1209/db/database.db')
        cursor = connection.cursor()
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
        tables = cursor.fetchall()
        print("Tabelle nel database:", tables)
        connection.close()
    except sqlite3.Error as e:
        print(f"Errore nella connessione al database: {e}")

test_db_connection()


# Inizializza il gestore di login
login_manager = LoginManager()
login_manager.init_app(app)

# Route LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Logica di autenticazione
        user_in_db = user_dao.get_user_by_username(username)
        print(f"User in DB: {user_in_db}")  # Debug: verifica cosa ritorna la funzione
        
        if user_in_db and check_password_hash(user_in_db['password'], password):
            user = User(
                id=user_in_db['id'],
                username=user_in_db['username'],
                password=user_in_db['password'],
                type=user_in_db['user_type']
            )
            login_user(user)
            flash('Login successful', 'success')
            print(f"Logged in as: {user.username}")  # Debug: conferma l'avvenuto login

            if user.type == 'personal_trainer':
                return redirect(url_for('home_personal'))
            else:
                return redirect(url_for('home_client'))
        else:
            flash('Invalid credentials', 'danger')
            print("Invalid credentials")  # Debug: credenziali non valide
            return redirect(url_for('login'))
    return render_template('login.html')

# LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Esegue il logout dell'utente
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Funzione di callback di Flask-Login per caricare l'utente
@login_manager.user_loader
def load_user(user_id):
    db_user = user_dao.get_user_by_id(user_id)  # Assicurati che questa funzione usi SQLite correttamente
    if db_user:
        return User(
            id=db_user['id'],
            username=db_user['username'],
            password=db_user['password'],
            type=db_user['user_type']
        )
    return None

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
# @login_required
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
        
        print("Form data received:", new_user_from_form)  # Print form data for debugging
        
        # Check if user already exists in the database
        user_in_db = user_dao.get_user_by_username(new_user_from_form.get('username'))
        if user_in_db:
            flash('C\'è già un utente registrato con questo nickname', 'danger')
            print(f"User already exists: {user_in_db}")  # Print existing user data
            return redirect(url_for('sign_up'))

        # Hash the user's password
        new_user_from_form['password'] = generate_password_hash(new_user_from_form.get('password'))
        print(f"Password hashed: {new_user_from_form['password']}")  # Print hashed password

        # Ensure all required fields are present
        if 'name' not in new_user_from_form or not new_user_from_form['name']:
            print("Error: 'name' field is missing or empty")
            flash('Il campo nome è obbligatorio', 'danger')
            return redirect(url_for('sign_up'))

        # Capture user role from the form
        new_user_from_form['role'] = new_user_from_form.get('role')
        print(f"User role: {new_user_from_form['role']}")  # Print user role

        # Save the new user in the database
        success = user_dao.create_user(new_user_from_form)

        if success:
            flash('New profile created', 'success')
            print("User successfully created")  # Print success message
            return redirect(url_for('base'))
        else:
            flash('Errore nella creazione del utente: riprova!', 'danger')
            print("Error creating user")  # Print error message
            return redirect(url_for('sign_up'))

    return render_template('signup.html')



# # Route LOGIN
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
        
#         # Logica di autenticazione
#         user_in_db = user_dao.get_user_by_username(username)
#         if user_in_db and check_password_hash(user_in_db['password'], password):
#             user = User(id=user_in_db['id'], username=user_in_db['username'], password=user_in_db['password'], type=user_in_db['user_type'])
#             login_user(user)
#             flash('Login successful', 'success')
#             if user.type == 'personal_trainer':
#                 return redirect(url_for('home_personal'))
#             else:
#                 return redirect(url_for('home_client'))
#         else:
#             flash('Invalid credentials', 'danger')
#             return redirect(url_for('login'))
#     return render_template('login.html')

# # LOGOUT
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()  # Questo è fornito da Flask-Login per effettuare il logout
#     flash('You have been logged out.', 'info')
#     return redirect(url_for('login'))

# @login_manager.user_loader
# def load_user(user_id):
#     db_user = user_dao.get_user_by_id(user_id)
#     if db_user:
#         return User(id=db_user['id'], username=db_user['username'], password=db_user['password'], type=db_user['user_type'])
#     return None

if __name__ == '__main__':
    app.run(debug=True)


#############################################
############# TODO ROUTE TESTING ############
# QUESTO è CODICE SPORCO, CI SONO RIGHE DA CANCELLARE CHE SI RIPETONO OGNI BLOCCO FORSE
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

############################################

# Rotte create_training_plan.hmtl
######## TODO CODICE SPORCO, RIGHE DA RIMUOVORE

# from flask import Flask, render_template, request, redirect, url_for, flash
# from models import db, Trainer, Client, Workout, TrainingPlan

# # Configurazione Flask
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = 'your_secret_key'

# # Inizializzazione del database
# db.init_app(app)

# # Rotta per mostrare il form di creazione della scheda di allenamento
# @app.route('/create_training_plan/<int:client_id>', methods=['GET', 'POST'])
# def create_training_plan(client_id):
#     # Verifica se l'utente è un personal trainer (autenticazione necessaria)
#     # Assumi che l'autenticazione sia gestita da un altro sistema
#     trainer = Trainer.query.filter_by(id=current_user.id).first()

#     if not trainer:
#         flash("Devi essere un personal trainer per creare una scheda di allenamento.")
#         return redirect(url_for('home'))

#     client = Client.query.get_or_404(client_id)

#     if request.method == 'POST':
#         title = request.form['title']
#         workout_ids = request.form.getlist('workouts')
        
#         if not title or not workout_ids:
#             flash("Tutti i campi sono obbligatori.")
#             return redirect(request.url)

#         # Filtra gli allenamenti selezionati per assicurare che appartengano al trainer o siano pubblici
#         selected_workouts = Workout.query.filter(Workout.id.in_(workout_ids), 
#                                                  (Workout.trainer_id == trainer.id) | (Workout.is_public == True)).all()

#         # Crea la nuova scheda di allenamento
#         new_plan = TrainingPlan(title=title, client_id=client_id, trainer_id=trainer.id)
#         db.session.add(new_plan)
#         db.session.commit()

#         # Associa gli allenamenti selezionati alla scheda
#         for workout in selected_workouts:
#             new_plan.workouts.append(workout)
#         db.session.commit()

#         flash("Scheda di allenamento creata con successo!")
#         return redirect(url_for('trainer_dashboard'))

#     # Recupera gli allenamenti disponibili per il trainer
#     workouts = Workout.query.filter((Workout.trainer_id == trainer.id) | (Workout.is_public == True)).all()
#     return render_template('create_training_plan.html', client=client, workouts=workouts)

# if __name__ == '__main__':
#     app.run(debug=True)

#########################################

# rotta delete_training_plan.html

# Rotta per mostrare la pagina di conferma eliminazione della scheda di allenamento
# @app.route('/delete_training_plan/<int:plan_id>', methods=['GET'])
# @login_required
# def show_delete_training_plan(plan_id):
#     # Verifica se l'utente è un personal trainer
#     trainer = Trainer.query.filter_by(id=current_user.id).first()

#     if not trainer:
#         flash("Devi essere un personal trainer per eliminare una scheda di allenamento.")
#         return redirect(url_for('home'))

#     training_plan = TrainingPlan.query.get_or_404(plan_id)

#     # Verifica che il training_plan appartenga al personal trainer
#     if training_plan.trainer_id != trainer.id:
#         flash("Non sei autorizzato ad eliminare questa scheda.")
#         return redirect(url_for('trainer_dashboard'))

#     return render_template('delete_training_plan.html', training_plan=training_plan)

# # Rotta per gestire l'eliminazione della scheda di allenamento
# @app.route('/delete_training_plan/<int:plan_id>', methods=['POST'])
# @login_required
# def delete_training_plan(plan_id):
#     trainer = Trainer.query.filter_by(id=current_user.id).first()

#     if not trainer:
#         flash("Devi essere un personal trainer per eliminare una scheda di allenamento.")
#         return redirect(url_for('home'))

#     training_plan = TrainingPlan.query.get_or_404(plan_id)

#     if training_plan.trainer_id != trainer.id:
#         flash("Non sei autorizzato ad eliminare questa scheda.")
#         return redirect(url_for('trainer_dashboard'))

#     # Elimina la scheda di allenamento
#     db.session.delete(training_plan)
#     db.session.commit()

#     flash("Scheda di allenamento eliminata con successo!")
#     return redirect(url_for('trainer_dashboard'))

# if __name__ == '__main__':
#     app.run(debug=True)

##########################################

# rotta delete_workout.html

# Rotta per mostrare la pagina di conferma eliminazione dell'allenamento
# @app.route('/delete_workout/<int:workout_id>', methods=['GET'])
# @login_required
# def show_delete_workout(workout_id):
#     # Verifica se l'utente è un personal trainer
#     trainer = Trainer.query.filter_by(id=current_user.id).first()

#     if not trainer:
#         flash("Devi essere un personal trainer per eliminare un allenamento.")
#         return redirect(url_for('home'))

#     workout = Workout.query.get_or_404(workout_id)

#     # Verifica che l'allenamento appartenga al personal trainer
#     if workout.trainer_id != trainer.id:
#         flash("Non sei autorizzato ad eliminare questo allenamento.")
#         return redirect(url_for('trainer_dashboard'))

#     return render_template('delete_workout.html', workout=workout)

# Rotta per gestire l'eliminazione dell'allenamento
# @app.route('/delete_workout/<int:workout_id>', methods=['POST'])
# @login_required
# def delete_workout(workout_id):
#     trainer = Trainer.query.filter_by(id=current_user.id).first()

#     if not trainer:
#         flash("Devi essere un personal trainer per eliminare un allenamento.")
#         return redirect(url_for('home'))

#     workout = Workout.query.get_or_404(workout_id)

#     # Verifica che l'allenamento appartenga al personal trainer
#     if workout.trainer_id != trainer.id:
#         flash("Non sei autorizzato ad eliminare questo allenamento.")
#         return redirect(url_for('trainer_dashboard'))

#     # Elimina l'allenamento
#     db.session.delete(workout)
#     db.session.commit()

#     flash("Allenamento eliminato con successo!")
#     return redirect(url_for('trainer_dashboard'))

# if __name__ == '__main__':
#     app.run(debug=True)


#####################################################

# rotta edit_training_plan.html

# Rotta per mostrare il modulo di modifica della scheda di allenamento
# @app.route('/edit_training_plan/<int:training_plan_id>', methods=['GET'])
# @login_required
# def show_edit_training_plan(training_plan_id):
#     trainer = Trainer.query.filter_by(id=current_user.id).first()

#     if not trainer:
#         flash("Devi essere un personal trainer per modificare una scheda di allenamento.")
#         return redirect(url_for('home'))

#     training_plan = TrainingPlan.query.get_or_404(training_plan_id)

#     # Verifica che la scheda appartenga al personal trainer
#     if training_plan.trainer_id != trainer.id:
#         flash("Non sei autorizzato a modificare questa scheda di allenamento.")
#         return redirect(url_for('trainer_dashboard'))

#     # Recupera gli allenamenti disponibili (pubblici e privati del trainer)
#     available_workouts = Workout.query.filter(
#         (Workout.public == True) | (Workout.trainer_id == trainer.id)
#     ).all()

#     # Allenamenti selezionati nella scheda
#     selected_workouts = [workout.id for workout in training_plan.workouts]

#     return render_template('edit_training_plan.html', training_plan=training_plan, available_workouts=available_workouts, selected_workouts=selected_workouts)

# Rotta per gestire la modifica della scheda di allenamento
# @app.route('/edit_training_plan/<int:training_plan_id>', methods=['POST'])
# @login_required
# def edit_training_plan(training_plan_id):
#     trainer = Trainer.query.filter_by(id=current_user.id).first()

#     if not trainer:
#         flash("Devi essere un personal trainer per modificare una scheda di allenamento.")
#         return redirect(url_for('home'))

#     training_plan = TrainingPlan.query.get_or_404(training_plan_id)

#     # Verifica che la scheda appartenga al personal trainer
#     if training_plan.trainer_id != trainer.id:
#         flash("Non sei autorizzato a modificare questa scheda di allenamento.")
#         return redirect(url_for('trainer_dashboard'))

#     # Aggiorna i dati della scheda di allenamento
#     training_plan.title = request.form['title']
#     training_plan.description = request.form['description']

#     # Aggiorna gli allenamenti della scheda
#     selected_workouts_ids = request.form.getlist('workouts')
#     selected_workouts = Workout.query.filter(Workout.id.in_(selected_workouts_ids)).all()
#     training_plan.workouts = selected_workouts

#     db.session.commit()

#     flash("Scheda di allenamento modificata con successo!")
#     return redirect(url_for('trainer_dashboard'))

# if __name__ == '__main__':
#     app.run(debug=True)


########################################

# editworkout.html


# Rotta per mostrare il modulo di modifica dell'allenamento
# @app.route('/edit_workout/<int:workout_id>', methods=['GET'])
# @login_required
# def show_edit_workout(workout_id):
#     trainer = Trainer.query.filter_by(id=current_user.id).first()

#     if not trainer:
#         flash("Devi essere un personal trainer per modificare un allenamento.")
#         return redirect(url_for('home'))

#     workout = Workout.query.get_or_404(workout_id)

#     # Verifica che l'allenamento appartenga al personal trainer
#     if workout.trainer_id != trainer.id:
#         flash("Non sei autorizzato a modificare questo allenamento.")
#         return redirect(url_for('trainer_dashboard'))

#     return render_template('edit_workout.html', workout=workout)

# # Rotta per gestire la modifica dell'allenamento
# @app.route('/edit_workout/<int:workout_id>', methods=['POST'])
# @login_required
# def edit_workout(workout_id):
#     trainer = Trainer.query.filter_by(id=current_user.id).first()

#     if not trainer:
#         flash("Devi essere un personal trainer per modificare un allenamento.")
#         return redirect(url_for('home'))

#     workout = Workout.query.get_or_404(workout_id)

#     # Verifica che l'allenamento appartenga al personal trainer
#     if workout.trainer_id != trainer.id:
#         flash("Non sei autorizzato a modificare questo allenamento.")
#         return redirect(url_for('trainer_dashboard'))

#     # Aggiorna i dati dell'allenamento
#     workout.title = request.form['title']
#     workout.description = request.form['description']
#     workout.level = request.form['level']
#     workout.public = 'public' in request.form  # True se il checkbox è selezionato

#     db.session.commit()

#     flash("Allenamento modificato con successo!")
#     return redirect(url_for('trainer_dashboard'))

# if __name__ == '__main__':
#     app.run(debug=True)


#############################################

# view_training_plan.html

# Rotta per visualizzare una scheda di allenamento
# @app.route('/view_training_plan/<int:training_plan_id>', methods=['GET'])
# @login_required
# def view_training_plan(training_plan_id):
#     training_plan = TrainingPlan.query.get_or_404(training_plan_id)

#     # Controllo dei permessi: solo il cliente o il personal trainer che ha creato la scheda possono vederla
#     if current_user.id not in [training_plan.client_id, training_plan.trainer_id]:
#         flash("Non sei autorizzato a visualizzare questa scheda di allenamento.")
#         return redirect(url_for('home'))

#     # Determina il tipo di utente: cliente o personal trainer
#     user_type = 'cliente' if hasattr(current_user, 'trainer_id') else 'trainer'

#     return render_template('view_training_plan.html', training_plan=training_plan, user_type=user_type)

# # Rotta per votare una scheda di allenamento
# @app.route('/rate_training_plan/<int:training_plan_id>', methods=['POST'])
# @login_required
# def rate_training_plan(training_plan_id):
#     training_plan = TrainingPlan.query.get_or_404(training_plan_id)

#     # Verifica che solo il cliente possa votare
#     if not hasattr(current_user, 'trainer_id') or current_user.id != training_plan.client_id:
#         flash("Non sei autorizzato a valutare questa scheda di allenamento.")
#         return redirect(url_for('home'))

#     # Ottieni il voto dal form
#     rating = int(request.form['rating'])

#     # Aggiorna il rating della scheda e del personal trainer
#     if rating < 1 or rating > 5:
#         flash("Il voto deve essere compreso tra 1 e 5.")
#         return redirect(url_for('view_training_plan', training_plan_id=training_plan_id))

#     # Aggiorna il rating nel database
#     training_plan.rating = rating
#     db.session.commit()

#     # Ricalcola il rating del personal trainer basato sulle schede
#     trainer = Trainer.query.get(training_plan.trainer_id)
#     ratings = [plan.rating for plan in trainer.training_plans if plan.rating is not None]
#     trainer.rating = sum(ratings) / len(ratings) if ratings else 0
#     db.session.commit()

#     flash("Valutazione inviata con successo!")
#     return redirect(url_for('client_dashboard'))

# if __name__ == '__main__':
#     app.run(debug=True)
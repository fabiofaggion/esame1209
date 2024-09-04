# from flask_login import UserMixin

# class User(UserMixin):
#    def __init__(self, id, username, password, user_type):
#         self.id = id
#         self.username = username
#         self.password = password
#         self.user_type = user_type


##########################################
####### TODO TEST MODELS #################
##########################################
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Modello per gli utenti, usato sia per i personal trainer che per i clienti
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # "trainer" o "client"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relazioni
    trainer_profile = relationship('Trainer', back_populates='user', uselist=False)
    client_profile = relationship('Client', back_populates='user', uselist=False)

    # Setter per la password (hashing)
    @property
    def password(self):
        raise AttributeError('La password non è un attributo leggibile')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Metodo per verificare la password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Metodo per identificare se l'utente è un trainer
    def is_trainer(self):
        return self.role == 'trainer'

    # Metodo per identificare se l'utente è un client
    def is_client(self):
        return self.role == 'client'

# Modello per i personal trainer
class Trainer(db.Model):
    __tablename__ = 'trainers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, default=0.0)

    # Relazioni
    user = relationship('User', back_populates='trainer_profile')
    workouts = relationship('Workout', back_populates='trainer')
    training_plans = relationship('TrainingPlan', back_populates='trainer')

# Modello per i clienti
class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.id'), nullable=True)

    # Relazioni
    user = relationship('User', back_populates='client_profile')
    trainer = relationship('Trainer', back_populates='training_plans', uselist=False)
    training_plans = relationship('TrainingPlan', back_populates='client')

# Modello per gli allenamenti
class Workout(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    level = db.Column(db.String(10), nullable=False)  # "facile", "medio", "difficile"
    public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relazioni
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.id'), nullable=False)
    trainer = relationship('Trainer', back_populates='workouts')

# Modello per le schede di allenamento
class TrainingPlan(db.Model):
    __tablename__ = 'training_plans'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relazioni
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    # Un piano di allenamento può includere molti allenamenti
    workouts = relationship('Workout', secondary='training_plan_workouts', back_populates='training_plans')
    trainer = relationship('Trainer', back_populates='training_plans')
    client = relationship('Client', back_populates='training_plans')

# Tabella di associazione per collegare TrainingPlan e Workout (molti-a-molti)
training_plan_workouts = db.Table('training_plan_workouts',
    db.Column('training_plan_id', db.Integer, db.ForeignKey('training_plans.id'), primary_key=True),
    db.Column('workout_id', db.Integer, db.ForeignKey('workouts.id'), primary_key=True)
)

# Funzione per aggiornare il rating del trainer
def update_trainer_rating(trainer_id):
    trainer = Trainer.query.get(trainer_id)
    if trainer:
        ratings = [plan.rating for plan in trainer.training_plans if plan.rating is not None]
        if ratings:
            trainer.rating = sum(ratings) / len(ratings)
        else:
            trainer.rating = 0
        db.session.commit()

from carlease import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    reservations = db.relationship('Reservation', backref="client", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

 
class Car(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title= db.Column(db.String(100), nullable=False)
    private = db.Column(db.String(60), nullable=False)
    car_picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    content =db.Column(db.Text, nullable=False)
    rents = db.relationship('Reservation', backref="car_lease", lazy=True)

    def __repr__(self):
        return f"Car('{self.title}', '{self.car_picture}', '{self.content}')"

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    details = db.Column(db.String(255))
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Reservation('{self.date_creation}', 'id number: {self.id}')"
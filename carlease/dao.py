# dao.py
from carlease import db, bcrypt
from carlease.models import User, Car, User_Verified

class UserDAO:
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_user(full_name, email, password):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(full_name=full_name, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()

class CarDAO:
    @staticmethod
    def create_car(model, color, license_plate, car_picture, kilometers, city):
        car = Car(model=model, color=color, license_plate=license_plate, car_picture=car_picture, kilometers=kilometers, city=city)
        db.session.add(car)
        db.session.commit()
        return car

    @staticmethod
    def get_car_by_id(car_id):
        return Car.query.get(car_id)


class User_VerifiedDAO:
    @staticmethod
    def get_userv_by_id(user_id):
        return User_Verified.query.get(user_id)

    @staticmethod
    def get_userv_by_phone(phone):
        return User_Verified.query.filter_by(phone=phone).first()

    @staticmethod
    def create_userv(phone, address):
        user_v = User_Verified(phone=phone, address=address)
        db.session.add(user_v)
        db.session.commit()
        return user_v

    @staticmethod
    def delete_userv(user_id):
        user_v = User_Verified.query.get(user_id)
        db.session.delete(user_v)
        db.session.commit()

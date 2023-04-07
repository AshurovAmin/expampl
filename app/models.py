from flask_login import UserMixin

from app import db, app, login_manager, bcrypt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    department = db.Column(db.String, unique=True, nullable=False)
    wage = db.Column(db.Integer)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    inn = db.Column(db.String, unique=True, nullable=False)
    position = db.relationship('Position', backref=db.backref('employee', lazy='dynamic'))
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)


    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, new_password):
        self.password_hash = bcrypt.generate_password_hash(new_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


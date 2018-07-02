from app import database as db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), index=True, unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=True)

    first_name = db.Column(db.String(120), index=True, unique=False, nullable=True)
    second_name = db.Column(db.String(120), index=True, unique=False, nullable=True)
    last_name = db.Column(db.String(120), index=True, unique=False, nullable=True)

    is_admin = db.Column(db.Boolean, index=True, unique=False, nullable=False, default=False)

    def __repr__(self):
        return '<User %r>' % self.name

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

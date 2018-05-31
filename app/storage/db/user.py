from storage.common.base import Format
from storage.db import db, generate_id, DbModel, Model
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model, DbModel):
    __tablename__ = 'users'
    id = db.Column(db.String(80), primary_key=True, default=generate_id)
    name = db.Column(db.String(80), index=True, unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=True)

    first_name = db.Column(db.String(120), index=True, unique=False, nullable=True)
    second_name = db.Column(db.String(120), index=True, unique=False, nullable=True)
    last_name = db.Column(db.String(120), index=True, unique=False, nullable=True)

    is_admin = db.Column(db.Boolean, index=True, unique=False, nullable=False, default=False)

    results = db.relationship("TestResult", backref="user", lazy="dynamic")

    def __repr__(self):
        return '<User %r>' % self.name

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        for param, value in kwargs.items():
            if param != 'password':
                setattr(self, param, value)
            else:
                self.set_password(value)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
    @hybrid_property
    def category(self):
        return 'Administrators' if self.is_admin else 'Users'

class Users(Model):
    type = User
    ids  = ['id', 'name']
    hide = ['password']
    filter = ['id', 'name', 'category', 'first_name', 'second_name', 'last_name', 'is_admin']

    save_callback = [{
        'func': 'set_password',
        'params': ['password']
    }]

    def verify_password(self, id, password):
        user = self.get(id=id, format=Format.RAW)
        if not user:
            return False
        return user.verify_password(password)

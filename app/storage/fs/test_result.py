from app import database as db
from datetime import datetime, date

class TestResult(db.Model):
    __tablename__ = 'test_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True, nullable=False)
    test_id = db.Column(db.String(120), index=True, unique=False, nullable=False)
    begin   = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow())
    end     = db.Column(db.DateTime, unique=False, nullable=True)
    last_item = db.Column(db.Integer, index=True, unique=False, nullable=False, default=1)
    score   = db.Column(db.Integer, index=True, unique=False, nullable=False, default=0)
    is_finished = db.Column(db.Boolean, index=True, unique=False, nullable=False, default=False)

    answers = db.relationship("TestAnswer", backref="test_results", lazy="dynamic")

    def __repr__(self):
        return '<TestResult %r>' % self.id

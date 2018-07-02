from app import database as db

class TestAnswer(db.Model):
    __tablename__ = 'test_answers'
    id        = db.Column(db.Integer, primary_key=True)
    item_no   = db.Column(db.Integer, index=True, nullable=False)
    result_id = db.Column(db.Integer, db.ForeignKey('test_results.id'), index=True, nullable=False)
    answer    = db.Column(db.Text, unique=False, nullable=True)
    result    = db.Column(db.Boolean, index=True, unique=False, nullable=False, default=False)
    time      = db.Column(db.DateTime, unique=False, nullable=False)

    def __repr__(self):
        return '<TestResult %r>' % self.id

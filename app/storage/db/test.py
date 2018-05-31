from storage.db import db, generate_id, DbModel, Model
from storage.common.base import current_second
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property

class Test(db.Model, DbModel):
    __tablename__ = 'tests'
    id = db.Column(db.String(80), primary_key=True, default=generate_id)
    name = db.Column(db.String(120), index=True, unique=True, nullable=False)
    category_id  = db.Column(db.String(80), db.ForeignKey('test_categories.id'), index=True, nullable=True)
    not_before   = db.Column(db.Date, nullable=True)
    not_after    = db.Column(db.Date, nullable=True)
    max_duration = db.Column(db.Integer,  nullable=True)
    items        = db.relationship("TestItem", backref="test", lazy="dynamic", cascade="all, delete-orphan")
    
    @hybrid_property
    def items_count(self):
        return self.items.count()

    results = db.relationship("TestResult", backref="test", lazy="dynamic")

    def __repr__(self):
        return '<Test %r>' % self.name

class TestItem(db.Model, DbModel):
    __tablename__ = 'tests_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_no = db.Column(db.Integer, index=True, nullable=False)
    test_id = db.Column(db.String(80), db.ForeignKey('tests.id'), index=True, nullable=False)
    content = db.Column(db.Text, nullable=True)

    answers = db.relationship("TestAnswer", backref="item", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return '<TestItem %r %r>' % (self.test_id, self.item_no)

class TestCategory(db.Model, DbModel):
    __tablename__ = 'test_categories'
    id = db.Column(db.String(80), primary_key=True, default=generate_id)
    name  = db.Column(db.String(120), index=True, unique=True, nullable=False)
    tests = db.relationship("Test", backref="category", lazy="dynamic", cascade="all, delete-orphan")
    def __repr__(self):
        return '<TestCategory %r>' % self.name

class TestResult(db.Model, DbModel):
    __tablename__ = 'test_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), db.ForeignKey('users.id'), index=True, nullable=False)
    test_id = db.Column(db.String(80), db.ForeignKey('tests.id'), index=True, nullable=False)
    begin   = db.Column(db.DateTime, unique=False, nullable=False, default=func.current_timestamp())
    end     = db.Column(db.DateTime, unique=False, nullable=True, default=func.current_timestamp(), onupdate=func.current_timestamp())
    last_item = db.Column(db.Integer, index=True, unique=False, nullable=False, default=1)
    is_finished = db.Column(db.Boolean, index=True, unique=False, nullable=False, default=False)

    @hybrid_property
    def score(self):
        return self.answers.filter_by(result=True).count()


    @hybrid_property
    def percent(self):
        return round(self.score / self.test.items_count * 100)
    
    @hybrid_property
    def mark(self):
        percent = int(self.percent)
        if percent >= 86:
            return 5
        if percent >= 70:
            return 4
        if percent >= 50:
            return 3
        if percent > 0:
            return 2
        return 1

    answers = db.relationship("TestAnswer", backref="test_results", lazy="dynamic")

    @hybrid_property
    def category(self):
        return 'Finished tests' if self.is_finished else 'Time over tests'

    def __repr__(self):
        return '<TestResult %r>' % self.id

class TestAnswer(db.Model, DbModel):
    __tablename__ = 'test_answers'
    id        = db.Column(db.Integer, primary_key=True)
    item_id   = db.Column(db.Integer, db.ForeignKey('tests_items.id'), index=True, nullable=False)
    result_id = db.Column(db.Integer, db.ForeignKey('test_results.id'), index=True, nullable=False)
    answer    = db.Column(db.Text, unique=False, nullable=True)
    result    = db.Column(db.Boolean, index=True, unique=False, nullable=False, default=False)
    time      = db.Column(db.DateTime, unique=False, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self):
        return '<TestAnswer %r>' % self.id

class Tests(Model):
    type     = Test
    category = TestCategory
    items    = TestItem
    ids      = ['id', 'name']
    hide     = ['category_id']
    filter   = ['id', 'name', '@category.name', 'items_count', 'not_before', 'not_after', 'max_duration']

class TestItems(Model):
    type     = TestItem
    filter   = ['id', 'item_no', 'content']

class TestResults(Model):
    type   = TestResult
    filter = ['id', 'test_id', 'begin', 'end', 'last_item', 'score', 'mark', 'percent', 'is_finished', 'category']
    ids    = ['user_id', 'test_id']

class TestAnswers(Model):
    type   = TestAnswer
    filter = ['answer', 'result', 'time']
    ids    = ['item_id', 'result_id']


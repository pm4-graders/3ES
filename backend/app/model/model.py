from peewee import Model, AutoField, CharField, IntegerField, FloatField, DateField, ForeignKeyField
from .database import db


def get_models():
    return [Candidate, Exam, Exercise]


class Candidate(Model):
    id = AutoField()
    number = CharField(max_length=20)
    date_of_birth = DateField()

    class Meta:
        database = db


class Exam(Model):
    id = AutoField()
    year = IntegerField()
    subject = CharField(max_length=100)
    total_score = FloatField()
    candidate = ForeignKeyField(Candidate, backref='exams')

    class Meta:
        database = db


class Exercise(Model):
    id = AutoField()
    number = IntegerField()
    score = FloatField()
    accuracy = FloatField()
    exam = ForeignKeyField(Exam, backref='exercises')

    class Meta:
        database = db

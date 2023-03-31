from peewee import *

database = SqliteDatabase('exam.db')


class Candidate(Model):
    candidate_id = AutoField()
    number = CharField(max_length=20)
    date_of_birth = DateField()

    class Meta:
        database = database


class Exam(Model):
    exam_id = AutoField()
    year = IntegerField()
    subject = CharField(max_length=100)
    total_score = FloatField()
    candidate_id = ForeignKeyField(Candidate, backref='exams')

    class Meta:
        database = database


class Exercise(Model):
    exercise_id = AutoField()
    number = IntegerField()
    score = FloatField()
    accuracy = FloatField()
    exam_id = ForeignKeyField(Exam, backref='exercises')

    class Meta:
        database = database

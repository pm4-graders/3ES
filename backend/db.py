from peewee import *

db = SqliteDatabase('exam.db')

class Candidate(Model):
    canditate_id = AutoField()
    birth_date = DateField()
    canditate_number = IntegerField()

    class Meta:
        database = db

class Exam(Model):
    exam_id = AutoField()
    exam_year = IntegerField()
    total_score = IntegerField()
    candidate_id = ForeignKeyField(Candidate, backref='exams')
    subject = CharField(100)

    class Meta:
        database = db

class Exercise(Model):
    exercise_id = AutoField()
    excerise_number = IntegerField()
    exercise_score = IntegerField()
    exam_id = ForeignKeyField(Exam, backref='exercises')

    class Meta:
        database = db

from peewee import *

db = SqliteDatabase('exam.db')

class Candidate(Model):
    name = CharField()
    class Meta:
        database = db

class Exam(Model):
    name = CharField()

    class Meta:
        database = db

class Exercise(Model):
    name = CharField()

    class Meta:
        database = db

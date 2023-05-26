from peewee import Model, AutoField, CharField, DateField, DateTimeField, FloatField, ForeignKeyField, IntegerField
import datetime
from .database import db
import util.constant as const


def get_models():
    return [Candidate, Exam, Exercise]


class BaseModel(Model):
    created_at = DateTimeField()
    updated_at = DateTimeField(null=True)

    def save(self, *args, **kwargs):

        now = datetime.datetime.utcnow().strftime(const.Data.TIMESTAMP_PATTERN)

        if self.created_at is None:
            self.created_at = now
        else:
            self.updated_at = now

        return super(BaseModel, self).save(*args, **kwargs)


class Candidate(BaseModel):
    id = AutoField()
    number = CharField(max_length=20)
    date_of_birth = DateField()

    class Meta:
        database = db


class Exam(BaseModel):
    id = AutoField()
    number = CharField(max_length=40)
    year = IntegerField()
    subject = CharField(max_length=100)
    score = FloatField()
    total_score = FloatField()
    confidence = FloatField()
    picture_path = CharField(max_length=255, default="")
    candidate = ForeignKeyField(Candidate, backref=const.Entity.EXAMS)

    class Meta:
        database = db


class Exercise(BaseModel):
    id = AutoField()
    number = CharField(max_length=10)
    score = FloatField()
    total_score = FloatField()
    confidence = FloatField()
    exam = ForeignKeyField(Exam, backref=const.Entity.EXERCISES)

    class Meta:
        database = db

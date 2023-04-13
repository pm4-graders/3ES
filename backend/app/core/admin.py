import core.database_handler as db
from model.model import Candidate, Exam, Exercise
from util.serializer import deserialize, serialize


def get_exams(year, subject):
    response = {"exams": []}

    query_exam = Exam.select()

    if year is not None:
        query_exam = query_exam.where(Exam.year == year)

    if subject is not None:
        query_exam = query_exam.where(Exam.subject == subject)

    for itr_exam_id in query_exam.iterator():
        response["exams"].append(Exam.get_by_id(itr_exam_id).__data__)

    return response


def get_exam(exam_id):

    # exam
    response = Exam.get_by_id(exam_id).__data__

    # candidate
    response.update({"candidate": Candidate.get_by_id(response["candidate"]).__data__})

    # exercise
    response.update({"exercises": []})
    query_exercise = Exercise.select().where(Exercise.exam == exam_id)
    for exercise_id in query_exercise.iterator():
        exercise = Exercise.get_by_id(exercise_id).__data__
        del exercise["exam"]
        response["exercises"].append(exercise)

    return response


def update_exam(exam_id, exam):
    return serialize({"success": db.update_exam(exam_id, exam)})


def update_exercise(exercise_id, exercise):
    return serialize({"success": db.update_exercise(exercise_id, exercise)})

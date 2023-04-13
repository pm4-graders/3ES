from model.model import Candidate, Exam, Exercise
from util.enum import Entity, Key


def save_scan_db(data):
    """
    Save a scan with all its entities
    """

    # candidate
    db_candidate = insert_candidate(data[Candidate.__name__.lower()])
    dict_insert_id(data, Candidate.__name__.lower(), db_candidate.id)

    # exams
    insert_exams(data[Entity.EXAMS.value], db_candidate)

    return data


def dict_insert_id(data, key, value):
    dictionary = {Key.ID.value: value}
    dictionary.update(data[key])
    data[key] = dictionary


def insert_candidate(candidate):
    db_candidate = Candidate.create(
        number=candidate[Candidate.number.name],
        date_of_birth=candidate[Candidate.date_of_birth.name]
    )

    return db_candidate


def insert_exams(exams, db_candidate):
    for index, exam in enumerate(exams):
        # exam
        db_exam = insert_exam(exam, db_candidate)
        dict_insert_id(exams, index, db_exam.id)
        # exercises
        insert_exercises(exam[Entity.EXERCISES.value], db_exam)


def insert_exam(exam, db_candidate):
    db_exam = Exam.create(
        year=exam[Exam.year.name],
        subject=exam[Exam.subject.name],
        total_score=exam[Exam.total_score.name],
        candidate=db_candidate
    )

    return db_exam


def update_exam(exam_id, exam):
    db_exam = Exam.get_or_none(exam_id)

    if db_exam is None:
        return False

    db_exam.total_score = exam.total_score
    db_exam.save()

    return True


def insert_exercises(exercises, db_exam):
    for index, exercise in enumerate(exercises):
        db_exercise = insert_exercise(exercise, db_exam)
        dict_insert_id(exercises, index, db_exercise.id)


def insert_exercise(exercise, db_exam):
    db_exercise = Exercise.create(
        number=exercise[Exercise.number.name],
        score=exercise[Exercise.score.name],
        accuracy=exercise[Exercise.accuracy.name],
        exam=db_exam
    )

    return db_exercise


def update_exercise(exercise_id, exercise):
    db_exercise = Exercise.get_or_none(exercise_id)

    if db_exercise is None:
        return False

    db_exercise.score = exercise.score
    db_exercise.save()

    return True

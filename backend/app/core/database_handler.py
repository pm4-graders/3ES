from peewee import DoesNotExist
from model.model import Candidate, Exam, Exercise
from util.enum import Entity


def insert_candidate(candidate):
    """
    DB insert for @Candidate
    """

    db_candidate = Candidate.create(
        number=candidate[Candidate.number.name],
        date_of_birth=candidate[Candidate.date_of_birth.name]
    )

    return db_candidate


def insert_exam(exam, db_candidate):
    """
    DB insert for @Exam
    """

    db_exam = Exam.create(
        year=exam[Exam.year.name],
        subject=exam[Exam.subject.name],
        total_score=exam[Exam.total_score.name],
        candidate=db_candidate
    )

    return db_exam


def insert_exams(exams, db_candidate):
    """
    Insert for exams with its exercises
    """

    db_exams = []

    for exam in exams:
        # exam
        db_exam = insert_exam(exam, db_candidate)
        if db_exam is not None:
            db_exams.append(db_exam)
            # exercises
            for exercise in exam[Entity.EXERCISES.value]:
                insert_exercise(exercise, db_exam)

    return db_exams


def insert_exercise(exercise, db_exam):
    """
    DB insert for @Exercise
    """

    db_exercise = Exercise.create(
        number=exercise[Exercise.number.name],
        score=exercise[Exercise.score.name],
        accuracy=exercise[Exercise.accuracy.name],
        exam=db_exam
    )

    return db_exercise


def read_candidate(candidate_id):
    """
    Read @Candidate
    """

    candidate = None

    try:
        candidate = Candidate.get_by_id(candidate_id).__data__
    except DoesNotExist:
        pass

    return candidate


def read_exam(exam_id):
    """
    Read @Exam
    """

    exam = None

    try:
        exam = Exam.get_by_id(exam_id).__data__
    except DoesNotExist:
        pass

    return exam


def read_exams(year, subject):
    """
    Get (search) exams for given parameters.
    """

    exams = []

    query_exam = Exam.select()

    if year is not None:
        query_exam = query_exam.where(Exam.year == year)

    if subject is not None:
        query_exam = query_exam.where(Exam.subject == subject)

    for exam_id in query_exam.iterator():
        try:
            exams.append(Exam.get_by_id(exam_id).__data__)
        except DoesNotExist:
            continue

    return exams


def read_exercises_by_exam(exam_id):
    """
    Read exercises by @Exam
    """

    exercises = []

    query_exercise = Exercise.select().where(Exercise.exam == exam_id)

    for exercise_id in query_exercise.iterator():
        try:
            exercise = Exercise.get_by_id(exercise_id).__data__
        except DoesNotExist:
            continue

        del exercise[Entity.EXAM.value]
        exercises.append(exercise)

    return exercises


def save_scan_db(data):
    """
    Save a scan with all its entities
    """

    exam_ids = []

    # candidate
    db_candidate = insert_candidate(data[Entity.CANDIDATE.value])

    if db_candidate is not None:
        # exams
        for db_exam in insert_exams(data[Entity.EXAMS.value], db_candidate):
            exam_ids.append(db_exam.id)

    return exam_ids


def update_exam(exam_id, exam):
    """
    DB update @Exam
    """

    try:
        db_exam = Exam.get_by_id(exam_id)
    except DoesNotExist:
        return False

    db_exam.total_score = exam.total_score
    db_exam.save()

    return True


def update_exercise(exercise_id, exercise, accuracy):
    """
    DB update @Exercise
    """

    try:
        db_exercise = Exercise.get_by_id(exercise_id)
    except DoesNotExist:
        return False

    db_exercise.score = exercise.score
    db_exercise.accuracy = accuracy
    db_exercise.save()

    return True

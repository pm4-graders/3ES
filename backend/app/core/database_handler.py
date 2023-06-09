from peewee import DoesNotExist
import core.cv_result as cv_res
from model.model import Candidate, Exam, Exercise
import util.constant as const


def delete_exam(exam_id):
    """
    Delete @Exam
    """

    try:
        db_exam = Exam.get_by_id(exam_id)
    except DoesNotExist:
        return False

    delete_exercise_by_exam(exam_id)

    db_exam.delete_instance()

    return True


def delete_exercise_by_exam(exam_id):
    """
    Delete all @Exercise data by @Exam
    """

    query_exercise = Exercise.delete().where(Exercise.exam == exam_id)
    query_exercise.execute()


def insert_exam(exam, db_candidate):
    """
    DB insert @Exam
    """

    # check existence using get_or_none
    db_exam = Exam.get_or_none(
        number=exam[Exam.number.name],
        year=exam[Exam.year.name],
        subject=exam[Exam.subject.name],
        # score=exam[Exam.score.name],
        # total_score=exam[Exam.total_score.name],
        # confidence=exam[Exam.confidence.name],
        # picture_path=exam[Exam.picture_path.name],
        candidate=db_candidate
    )

    if db_exam is None:
        # insert
        db_exam = Exam.create(
            number=exam[Exam.number.name],
            year=exam[Exam.year.name],
            subject=exam[Exam.subject.name],
            score=exam[Exam.score.name],
            total_score=exam[Exam.total_score.name],
            confidence=exam[Exam.confidence.name],
            picture_path=exam[Exam.picture_path.name],
            candidate=db_candidate,
        )
    else:
        # existing
        db_exam = None

    return db_exam


def insert_exercise(exercise, db_exam):
    """
    DB insert @Exercise
    """

    # check existence using get_or_none
    db_exercise = Exercise.get_or_none(
        number=exercise[Exercise.number.name],
        # score=exercise[Exercise.score.name],
        # total_score=exercise[Exercise.total_score.name],
        # confidence=exercise[Exercise.confidence.name],
        exam=db_exam
    )

    if db_exercise is None:
        # insert
        db_exercise = Exercise.create(
            number=exercise[Exercise.number.name],
            score=exercise[Exercise.score.name],
            total_score=exercise[Exercise.total_score.name],
            confidence=exercise[Exercise.confidence.name],
            exam=db_exam
        )
    else:
        # existing
        db_exercise = None

    return db_exercise


def insert_or_get_candidate(candidate):
    """
    DB insert or get @Candidate
    """

    # check existence using get_or_none
    db_candidate = Candidate.get_or_none(
        number=candidate[Candidate.number.name],
        date_of_birth=candidate[Candidate.date_of_birth.name]
    )

    if db_candidate is None:
        # insert
        db_candidate = Candidate.create(
            number=candidate[Candidate.number.name],
            date_of_birth=candidate[Candidate.date_of_birth.name]
        )

    return db_candidate


def read_candidate(candidate_id):
    """
    Read @Candidate data
    """

    candidate = None

    try:
        candidate = Candidate.get_by_id(candidate_id).__data__
    except DoesNotExist:
        pass

    return candidate


def read_exam(exam_id):
    """
    Read @Exam data
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

        exam = read_exam(exam_id)

        if exam is not None:
            exams.append(exam)

    return exams


def read_exercises_by_exam(exam_id):
    """
    Read all @Exercise data by @Exam
    """

    exercises = []

    query_exercise = Exercise.select().where(Exercise.exam == exam_id)

    for exercise_id in query_exercise.iterator():
        exercise = Exercise.get_by_id(exercise_id).__data__
        del exercise[Exercise.exam.name]
        exercises.append(exercise)

    return exercises


def read_logical_exams(year, subject):
    """
    Get (search) logical exams for given parameters.
    """

    logical_exams = []

    query_exam = Exam.select(Exam.year, Exam.subject).distinct()

    if year is not None:
        query_exam = query_exam.where(Exam.year == year)

    if subject is not None:
        query_exam = query_exam.where(Exam.subject == subject)

    for logical_exam in query_exam.iterator():
        logical_exams.append(logical_exam)

    return logical_exams


def save_scan_db(cv_data: cv_res.CVResult):
    """
    Save a scan with all its entities
    """

    exam_id = None

    # candidate
    db_candidate = insert_or_get_candidate(vars(cv_data.candidate))

    if db_candidate is not None:

        # exam
        exam = vars(cv_data.exam)
        print(exam)
        db_exam = insert_exam(exam, db_candidate)

        if db_exam is not None:

            exam_id = db_exam.id

            # exercises
            for exercise in exam[const.Entity.EXERCISES]:
                insert_exercise(vars(exercise), db_exam)

    return exam_id


def update_exam(exam_id, exam, confidence):
    """
    DB update @Exam
    """

    try:
        db_exam = Exam.get_by_id(exam_id)
    except DoesNotExist:
        return False

    db_exam.score = exam.score
    db_exam.confidence = confidence
    db_exam.save()

    return True


def update_exercise(exercise_id, exercise, confidence):
    """
    DB update @Exercise
    """

    try:
        db_exercise = Exercise.get_by_id(exercise_id)
    except DoesNotExist:
        return False

    db_exercise.score = exercise.score
    db_exercise.confidence = confidence
    db_exercise.save()

    return True

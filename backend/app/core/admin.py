from api.schema import BaseResponse, Candidate, Exam, ExamFull, ExamFullResponse, ExamFullListResponse, Exercise
import core.database_handler as db
import model.model as model
import util.constant as const


def build_exam_full(exam):
    """
    Build exam with all its relationships
    """

    # candidate
    candidate = db.read_candidate(exam[model.Exam.candidate.name])

    exam_rs = ExamFull(
        id=exam[model.Exam.id.name],
        year=exam[model.Exam.year.name],
        subject=exam[model.Exam.subject.name],
        total_score=exam[model.Exam.total_score.name],
        candidate=Candidate(
            id=candidate[model.Candidate.id.name],
            number=candidate[model.Candidate.number.name],
            date_of_birth=candidate[model.Candidate.date_of_birth.name]
        ),
        exercises=[]
    )

    # exercises
    for exercise in db.read_exercises_by_exam(exam[model.Exam.id.name]):
        exam_rs.exercises.append(exercise)

    return exam_rs


def get_exam_full(exam_id):
    """
    Get exam and all its relationships
    """

    # exam response
    exam_rs = None

    # exam
    exam = db.read_exam(exam_id)

    if exam is not None:
        exam_rs = build_exam_full(exam)

    # response
    if exam_rs:
        return ExamFullResponse(success=True, exam=exam_rs)
    else:
        return ExamFullResponse(success=False)


def get_exams(year, subject):
    """
    Get (search) exams for given parameters.
    """

    exams_rs = []

    for exam in db.read_exams(year, subject):
        exams_rs.append(build_exam_full(exam))

    return ExamFullListResponse(
        success=True if exams_rs else False,
        exams=exams_rs
    )


def update_exam(exam_id, exam):
    """
    Update existing exam
    """

    return BaseResponse(success=db.update_exam(exam_id, exam))


def update_exercise(exercise_id, exercise):
    """
    Update existing exercise
    """

    return BaseResponse(success=db.update_exercise(exercise_id, exercise, const.Exercise.ACCURACY_MAX))

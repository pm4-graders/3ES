import datetime, os, uuid
from fastapi import UploadFile
from api.schema import BaseResponse, ExamFullResponse
from .admin import get_exam_full
import core.cv_result as cv_res
import core.database_handler as db
import util.constant as const

IMAGEDIR = "images/"


def save_scan(file: UploadFile):
    """
    Save a scan by storing the file into the file storage, request extraction with cv module,
    validate and save the data into the db.
    """

    # save image to file system
    create_upload_file(file)

    # call computer vision
    try:

        # mock-impl. to continue implementation of response handling
        # cv_rs = DigitRecognizer().recognize_digits_in_photo(photo={})
        cv_data = get_dummy_cv_result()

    except Exception as exc:
        raise Exception(const.Message.CV_EXCEPTION.format(exc))

    # validation
    message = validate_cv_result(cv_data)

    # database save
    exam_id = db.save_scan_db(cv_data)

    if not exam_id:
        raise Exception(const.Message.EXAM_EXISTS)

    # get exam data
    response = get_exam_full(exam_id)

    if response.message is None:
        response.message = message

    return response


def save_scan_wrapper(file: UploadFile):
    """
    Wrapper of save_scan
    """

    try:

        response = save_scan(file)

    except Exception as exc:
        response = BaseResponse(success=False, message=str(exc))

    return response


def validate_cv_result(cv_data):
    """
    Validate CV result. Returns a message in case of failure.
    """

    message = None

    if cv_data.exam.score != cv_data.exam.calc_exercises_score():
        message = const.Validation.W_SCORE_EQ

    return message


def get_dummy_cv_result():
    """
    Create and return a cv result with dummy values.
    """

    import json

    json_data = '{"candidate":{"number":"CHSG-23.123","date_of_birth":"2010-01-01"},"exam":{"year":2023,' \
                '"subject":"ABC English","score":4,"confidence":0.91, "exercises":[{"number":"1.a","score":1.75,' \
                '"confidence":0.88},{"number":"1.b","score":2.00,"confidence":0.98}]}}'

    data_dict = json.loads(json_data)

    candidate_data = data_dict['candidate']
    candidate = cv_res.Candidate(candidate_data['number'], candidate_data['date_of_birth'])

    exam_data = data_dict['exam']
    exercises = []
    for exercise_data in exam_data['exercises']:
        exercise = cv_res.Exercise(exercise_data['number'], exercise_data['score'], exercise_data['confidence'])
        exercises.append(exercise)

    exam = cv_res.Exam(exam_data['year'], exam_data['subject'], exam_data['score'],  exam_data['confidence'], exercises)

    return cv_res.CVResult(candidate, exam)


def create_directories(exists, path):
    """
    Create directory if not existing
    """

    if not exists:
        if not os.path.exists(IMAGEDIR):
            os.mkdir(IMAGEDIR)
        os.mkdir(path)


def create_upload_file(file: UploadFile):
    """
    Save file into directory
    """

    try:
        file.filename = f"{uuid.uuid4()}.jpg"
        contents = file.read()

        # Get the current year
        today = datetime.date.today()
        year = today.year
        path = f"{IMAGEDIR}{year}"
        exists = os.path.exists(path)

        # Create the directories if they do not exist
        create_directories(exists, path)

        # Save the file
        save_file(contents, year, file.filename)

        return {"filename": file.filename}
    except Exception as exc:
        return {"error": "An error occurred while processing the uploaded file"}


def save_file(contents, year, filename):
    """
    Write file
    """

    with open(f"{IMAGEDIR}/{year}/{filename}", "wb") as f:
        f.write(contents)

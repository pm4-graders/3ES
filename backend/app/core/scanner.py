from fastapi import APIRouter, File, UploadFile
import datetime, os, uuid, logging
import core.database_handler as db
from api.schema import BaseResponse, ExamFullResponse
from .admin import get_exam_full
import core.cv_result as cv_res
import core.database_handler as db
from util.serializer import deserialize, serialize


IMAGEDIR = "images/"



def save_scan(file: UploadFile = File(...)):
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
        raise Exception(f"Computer Vision: {exc}")

    # validation
    message = validate_cv_result(cv_data)

    # database save
    exam_id = db.save_scan_db(cv_data)

    if not exam_id:
        raise Exception("Exam already exists")

    # get exam data
    response = get_exam_full(exam_id)

    if response.message is None:
        response.message = message

    return response


def save_scan_wrapper():
    """
    Wrapper of save_scan
    """

    try:

        response = save_scan()

    except Exception as exc:
        response = BaseResponse(success=False, message=str(exc))

    return response


def validate_cv_result(cv_data):
    """
    Validate CV result. Returns a message in case of failure.
    """

    message = None

    if cv_data.exam.total_score != cv_data.exam.calc_total_score():
        message = "Warning: The total score of the exam is unequal to the sum of the scores of the associated exercises"

    return message


def get_dummy_cv_result():
    """
    Create and return a cv result with dummy values.
    """

    json_data = '{"candidate":{"number":"CHSG-23.123","date_of_birth":"2010-01-01"},"exam":{"year":2023,' \
                '"subject":"ABC English","total_score":4,"exercises":[{"number":"1.a","score":1.75,' \
                '"accuracy":0.88},{"number":"1.b","score":2.00,"accuracy":0.98}]}}'

    data_dict = deserialize(json_data)

    candidate_data = data_dict['candidate']
    candidate = cv_res.Candidate(candidate_data['number'], candidate_data['date_of_birth'])

    exam_data = data_dict['exam']
    exercises = []
    for exercise_data in exam_data['exercises']:
        exercise = cv_res.ExamExercise(exercise_data['number'], exercise_data['score'], exercise_data['accuracy'])
        exercises.append(exercise)

    exam = cv_res.Exam(exam_data['year'], exam_data['subject'], exam_data['total_score'], exercises)

    return cv_res.CVResult(candidate, exam)

ef create_upload_file(file: UploadFile = File(...)):
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
    except Exception as e:
        logger.exception("An error occurred while processing the uploaded file")
        return {"error": "An error occurred while processing the uploaded file"}


def create_directories(exists, path):
    if not exists:
        if not os.path.exists(IMAGEDIR):
            os.mkdir(IMAGEDIR)
        os.mkdir(path)

def save_file(contents, year, filename):
    with open(f"{IMAGEDIR}/{year}/{filename}", "wb") as f:
        f.write(contents)
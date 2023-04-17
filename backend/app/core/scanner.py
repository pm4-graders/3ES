from api.schema import BaseResponse, ExamFullResponse
from .admin import get_exam_full
import core.cv_result as cv_res
import core.database_handler as db
from util.serializer import deserialize, serialize


def save_scan():
    """
    Save a scan by storing the file into the file storage, request extraction with cv module,
    save the data into the db and return a json.
    """

    # save image to file system

    # call computer vision
    try:

        # mock-impl. to continue implementation of response handling
        # cv_rs = DigitRecognizer().recognize_digits_in_photo(photo={})
        cv_data = get_dummy_cv_result()

    except Exception as exc:
        # response
        return ExamFullResponse(success=False, message=f"Computer Vision: {exc}")

    # build response
    message = validate_cv_result(cv_data)

    # save response to database
    exam_id = db.save_scan_db(cv_data)

    if exam_id:

        # get exam data
        exam_full_response = get_exam_full(exam_id)

        if exam_full_response.message is None:
            exam_full_response.message = message

        # response
        return exam_full_response

    else:
        return BaseResponse(success=False, message="Exam already exists")


def validate_cv_result(cv_data):
    """
    Validate CV result. Returns a message in case of failure.
    """

    message = None

    if cv_data is None:
        message = "CV Error"
    else:
        message = "Gud"

    return message


def get_dummy_cv_result():
    """
    Create and return a cv result with dummy values.
    """

    json_data = '{"candidate":{"number":"CHSG-23.1231","date_of_birth":"2010-01-01"},"exam":{"year":2023,' \
                '"subject":"ABC English","total_score":3.75,"exercises":[{"number":"1.a","score":1.75,' \
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

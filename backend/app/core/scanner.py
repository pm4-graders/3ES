import core.database_handler as db
from .admin import get_exam_full
from util.serializer import deserialize, serialize

cv_rs_dummy_json = '{"candidate":{"number":"CHSG-23.123","date_of_birth":"2010-01-01"},"exam":{"year":2023,' \
                   '"subject":"ABC English","total_score":3.75,"exercises":[{"number":"1.a","score":1.75,' \
                   '"accuracy":0.88},{"number":"1.b","score":2.00,"accuracy":0.98}]}}'


def save_scan():
    """
    Save a scan by storing the file into the file storage, request extraction with cv module,
    save the data into the db and return a json.
    """

    # save image to file system

    # call computer vision
    # mock-impl. to continue implementation of response handling
    # cv_rs = DigitRecognizer().recognize_digits_in_photo(photo={})
    cv_rs = deserialize(cv_rs_dummy_json)

    # save response to database
    exam_id = db.save_scan_db(cv_rs)

    # response
    return get_exam_full(exam_id)

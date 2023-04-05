from backend.app.util.serializer import deserialize, serialize
from .scanner_db import save_scan_db

cv_rs_dummy_json = '{"candidate":{"number":"CHSG-23.123","date_of_birth":"2010-01-01"},"exams":[{"year":2023,' \
                   '"subject":"ABC English","total_score":3.75,"exercises":[{"number":"1.a","score":1.75,' \
                   '"accuracy":0.88},{"number":"1.b","score":2.00,"accuracy":0.98}]},{"year":2023,"subject":"123 ' \
                   'Math","total_score":9.50,"exercises":[{"number":"1","score":4.50,"accuracy":0.75},{"number":"2",' \
                   '"score":5.00,"accuracy":0.95}]}]}'


def save_scan():
    """
    Save a scan by storing the file into the file storage, request extration with cv module, save the data into the db and return a json.
    """

    # save image to file system

    # call computer vision
    cv_rs = None
    # cv_rs = DigitRecognizer().recognize_digits_in_frame(video_stream={})
    # cv_rs = DigitRecognizer().recognize_digits_in_photo(photo={})
    # mock-impl. to continue implementation of response handling
    if cv_rs is None:
        print("cv_rs is none")
        cv_rs = deserialize(cv_rs_dummy_json)

    # save response to database
    db_rs = save_scan_db(cv_rs)

    # return response
    return serialize(db_rs)

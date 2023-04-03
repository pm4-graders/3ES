from backend.app.util.serializer import deserialize, serialize
from .scanner_db import save_scan_db

cv_rs_dummy_json = '{"candidate":{"number":"CHSG-23.123","date_of_birth":"2010-01-01"},"exams":[{"year":2023,' \
                   '"subject":"ABC English","total_score":3.75,"exercises":[{"number":"1.a","score":1.75,' \
                   '"accuracy":0.88},{"number":"1.b","score":2.00,"accuracy":0.98}]},{"year":2023,"subject":"123 ' \
                   'Math","total_score":9.50,"exercises":[{"number":"1","score":4.50,"accuracy":0.75},{"number":"2",' \
                   '"score":5.00,"accuracy":0.95}]}]}'


def save_scan():
    """
    TODO
    """

    # save image to file system
    # TODO - Issue #15

    # call computer vision
    # TODO - Issue #17
    # mock-impl. to continue implementation of response handling
    cv_rs = deserialize(cv_rs_dummy_json)

    # save response to database
    db_rs = save_scan_db(cv_rs)

    # return response
    return serialize(db_rs)

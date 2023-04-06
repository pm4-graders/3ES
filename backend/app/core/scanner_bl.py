from util.serializer import deserialize, serialize
from core.scanner_db import save_scan_db
from fastapi import APIRouter, File, UploadFile
import datetime, os, uuid

IMAGEDIR = "images/"

cv_rs_dummy_json = '{"candidate":{"number":"CHSG-23.123","date_of_birth":"2010-01-01"},"exams":[{"year":2023,' \
                   '"subject":"ABC English","total_score":3.75,"exercises":[{"number":"1.a","score":1.75,' \
                   '"accuracy":0.88},{"number":"1.b","score":2.00,"accuracy":0.98}]},{"year":2023,"subject":"123 ' \
                   'Math","total_score":9.50,"exercises":[{"number":"1","score":4.50,"accuracy":0.75},{"number":"2",' \
                   '"score":5.00,"accuracy":0.95}]}]}'


def save_scan(file: UploadFile = File(...)):
    """
    Save a scan by storing the file into the file storage, request extraction with cv module,
    save the data into the db and return a json.
    """

    # save image to file system
    create_upload_file(file)
    # call computer vision
    # mock-impl. to continue implementation of response handling
    # cv_rs = DigitRecognizer().recognize_digits_in_photo(photo={})
    cv_rs = deserialize(cv_rs_dummy_json)

    # save response to database
    db_rs = save_scan_db(cv_rs)

    # respond with json
    return serialize(db_rs)


async def create_upload_file(file: UploadFile = File(...)):
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()
    #for folder get year
    today = datetime.date.today()
    year = today.year
    path = f"{IMAGEDIR}{year}"
    exists = os.path.exists(path)
    if not exists:
        if not os.path.exists(IMAGEDIR):
            os.mkdir(IMAGEDIR)
        os.mkdir(path)
    # save the file
    with open(f"{IMAGEDIR}/{year}/{file.filename}", "wb") as f:
        f.write(contents)
# TODO: bild als base64 an tobis klasse übergeben
    return {"filename": file.filename}

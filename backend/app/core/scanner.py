from fastapi import APIRouter, File, UploadFile
import datetime, os, uuid, logging
import core.database_handler as db
from .admin import get_exam_full
from util.serializer import deserialize, serialize

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

IMAGEDIR = "images/"

cv_rs_dummy_json = '{"candidate":{"number":"CHSG-23.123","date_of_birth":"2010-01-01"},"exam":{"year":2023,' \
                   '"subject":"ABC English","total_score":3.75,"exercises":[{"number":"1.a","score":1.75,' \
                   '"accuracy":0.88},{"number":"1.b","score":2.00,"accuracy":0.98}]}}'


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
    exam_id = db.save_scan_db(cv_rs)

    # response
    return get_exam_full(exam_id)

#

def create_upload_file(file: UploadFile = File(...)):
    try:
        print("3")

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

        # TODO: bild als base64 an tobis klasse übergeben
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
    print("8")

    with open(f"{IMAGEDIR}/{year}/{filename}", "wb") as f:
        print("9")
        f.write(contents)
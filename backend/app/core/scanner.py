import asyncio
import datetime, os, uuid
from fastapi import UploadFile
from api.schema import BaseResponse, ExamFullResponse

import sys

sys.path.append(sys.path[0] + '/../../')
sys.path.append(sys.path[0] + '/../../cv/')
from cv.DigitRecognizer import DigitRecognizer

from .admin import get_exam_full
import core.cv_result as cv_res
import core.database_handler as db
import util.constant as const
import nest_asyncio
import cv2

nest_asyncio.apply()

recognizer = DigitRecognizer()

IMAGEDIR = "images/"


def save_scan(file: UploadFile):
    """
    Save a scan by storing the file into the file storage, request extraction with cv module,
    validate and save the data into the db.
    """

    # save image to file system
    loop = asyncio.get_event_loop()
    coroutine = create_upload_file_async(file)
    picture_path = loop.run_until_complete(coroutine)

    # call computer vision
    try:
        image = cv2.imread(picture_path)
        print("image", image)
        exam_object = recognizer.recognize_digits_in_photo(image)
    except Exception as exc:
        print(exc)
        raise Exception(const.Message.CV_EXCEPTION.format(exc))

    # validation
    message = validate_cv_result(exam_object)

    # database save
    exam_id = db.save_scan_db(exam_object)

    if not exam_id:
        raise Exception(const.Message.EXAM_EXISTS)

    # get exam data
    response = get_exam_full(exam_id)

    # response message handling
    if message:
        if response.message:
            response.message.extend(message)
        else:
            response.message = message

    return response


def save_scan_wrapper(file: UploadFile):
    """
    Wrapper of save_scan
    """

    try:

        response = save_scan(file)

    except Exception as exc:
        response = BaseResponse(success=False, message=[str(exc)])

    return response


def validate_cv_result(cv_data):
    """
    Validate CV result. Returns a message in case of failure.
    """

    message = []

    # 1 - check exam score with sum(exercise.score)
    if cv_data.exam.score != cv_data.exam.calc_exercises_score():
        message.append(const.Validation.W_EXA_SCORE_EQ)

    # 2 - check each exercise score with its max_score
    for exercise in cv_data.exam.exercises:
        if exercise.score > exercise.max_score:
            message.append(const.Validation.W_EXE_SCORE_EQ.format(exercise.number))

    return message


def get_dummy_cv_result():
    """
    Create and return a cv result with dummy values.
    """

    import json

    json_data = '{"candidate":{"number":"CHSG-23.123","date_of_birth":"2010-01-01"},"exam":{"year":2023,' \
                '"subject":"ABC English","score":4.00,"confidence":0.91, "exercises":[{' \
                '"number":"1.a","score":2.75,"confidence":0.88,"max_score":3},{"number":"1.b","score":2.00,' \
                '"confidence":0.98,"max_score":1}]},"result_validated":true} '

    data_dict = json.loads(json_data)

    candidate_data = data_dict['candidate']
    candidate = cv_res.Candidate(candidate_data['number'], candidate_data['date_of_birth'])

    exam_data = data_dict['exam']
    exercises = []
    for exercise_data in exam_data['exercises']:
        exercise = cv_res.Exercise(exercise_data['number'], exercise_data['score'], exercise_data['confidence'],
                                   exercise_data['max_score'])
        exercises.append(exercise)

    exam = cv_res.Exam(exam_data['year'], exam_data['subject'], exam_data['score'], exam_data['confidence'], exercises)

    return cv_res.CVResult(candidate, exam, data_dict['result_validated'])


async def save_file_async(file: UploadFile, year: int, filename: str):
    """
    Asynchronously save file into directory
    """

    path = f"{IMAGEDIR}{year}/{filename}"
    with open(path, "wb") as buffer:
        buffer.write(await file.read())


async def create_upload_file_async(file: UploadFile):
    """
    Creates folder and calls function to save the picture asynchronously
    """

    try:
        file.filename = f"{uuid.uuid4()}.jpg"

        # Get the current year
        today = datetime.date.today()
        year = today.year
        path = f"{IMAGEDIR}{year}"
        exists = os.path.exists(path)

        # Create the directories if they do not exist
        if not exists:
            if not os.path.exists(IMAGEDIR):
                os.mkdir(IMAGEDIR)
            os.mkdir(path)

        # Save the file asynchronously
        await save_file_async(file, year, file.filename)

        return path + "/" + file.filename
    except Exception as exc:
        return {"error": "An error occurred while processing the uploaded file"}

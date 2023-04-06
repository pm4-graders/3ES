from fastapi import APIRouter, File, UploadFile
import datetime, os, uuid
import core.scanner_bl as scanner
from model.model import Candidate, Exam, Exercise

router = APIRouter()
IMAGEDIR = "images/"

@router.post("/scan/save")
async def function_scan_save():
    return scanner.save_scan()


@router.get("/candidates")
async def function_get_candidates():
    return Candidate.get()


@router.post("/candidate/{name}")
async def post_candidate(name: str):
    return Candidate.create({name})


@router.get("/exams")
async def get_exams():
    return Exam.get()


@router.post("/exams/{name}")
async def post_candidate(name: str):
    return Exam.create({name})


@router.post("/exercises/{name}")
async def post_exercise(name: str):
    return Exercise.create({name})


@router.get("/exercise")
async def get_exercise():
    return Exercise.get()


@router.post("/upload/")
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

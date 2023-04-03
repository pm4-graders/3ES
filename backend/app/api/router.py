from fastapi import APIRouter

import backend.app.core.scanner_bl as core_scanner
from backend.app.model.model import Candidate, Exam, Exercise

router = APIRouter()


@router.post("/scanner/save")
async def function_save():
    return core_scanner.save_scan()


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
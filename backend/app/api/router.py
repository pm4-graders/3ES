from fastapi import APIRouter
from pydantic import BaseModel

import core.admin as admin
import core.scanner as scanner

router = APIRouter(
    prefix='/api'
)


class ExamTotalScore(BaseModel):
    total_score: int


class ExerciseScore(BaseModel):
    score: int


@router.post("/scan/save")
async def post_scan_save():
    return scanner.save_scan()


@router.get("/exams")
async def get_exams(year: int = None, subject: str = None):
    return admin.get_exams(year, subject)


@router.get("/exams/{examId}")
async def get_exam(examId: int):
    return admin.get_exam(examId)


@router.post("/exams/{examId}")
async def post_exam(examId: int, exam: ExamTotalScore):
    return admin.update_exam(examId, exam)


@router.post("/exercises/{exercisesId}")
async def post_exercise(exercisesId: int, exercise: ExerciseScore):
    return admin.update_exercise(exercisesId, exercise)

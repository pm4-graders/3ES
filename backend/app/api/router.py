from fastapi import APIRouter, HTTPException
from .schema import BaseResponse, ExamFullResponse, ExamFullListResponse, ExamTotalScore, ExerciseScore
import core.admin as admin
import core.scanner as scanner
import util.constant as const

router = APIRouter(
    prefix='/api'
)


@router.post("/scan/save", response_model=ExamFullResponse, response_model_exclude_none=True)
async def post_scan_save():
    return scanner.save_scan_wrapper()


@router.get("/exams/{examId}", response_model=ExamFullResponse, response_model_exclude_none=True)
async def get_exam(examId: int):
    """
    Get exam and all its relationships
    """

    response = admin.get_exam_full(examId)

    if not response.success:
        raise HTTPException(status_code=404, detail=const.Message.EXAM_NOT_FOUND.format(examId))

    return response


@router.post("/exams/{examId}", response_model=BaseResponse, response_model_exclude_none=True)
async def post_exam(examId: int, exam: ExamTotalScore):
    """
    Update existing exam
    """

    response = admin.update_exam(examId, exam)

    if not response.success:
        raise HTTPException(status_code=404, detail=const.Message.EXAM_NOT_FOUND.format(examId))

    return response


@router.get("/exams", response_model=ExamFullListResponse, response_model_exclude_none=True)
async def get_exams(year: int = None, subject: str = None):
    """
    Get (search) exams for given parameters.
    """

    response = admin.get_exams(year, subject)

    if not response.success:
        raise HTTPException(status_code=404, detail=const.Message.EXAMS_NOT_FOUND)

    return response


@router.post("/exercises/{exercisesId}", response_model=BaseResponse, response_model_exclude_none=True)
async def post_exercise(exercisesId: int, exercise: ExerciseScore):
    """
    Update existing exercise
    """

    response = admin.update_exercise(exercisesId, exercise)

    if not response.success:
        raise HTTPException(status_code=404, detail=const.Message.EXERCISE_NOT_FOUND.format(exercisesId))

    return response

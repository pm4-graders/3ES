from fastapi import APIRouter, HTTPException, UploadFile, File, FastAPI
from .schema import BaseResponse, ExamFullResponse, ExamFullListResponse, LogicalExamListResponse, Score
import core.admin as admin
import core.scanner as scanner
import util.constant as const

router = APIRouter(
    prefix='/api'
)


@router.get("/exams/{examId}", response_model=ExamFullResponse, response_model_exclude_none=True)
async def get_exam(examId: int):
    """
    Get exam and all its relationships
    """

    response = admin.get_exam_full(examId)

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


@router.get("/logical-exams", response_model=LogicalExamListResponse, response_model_exclude_none=True)
async def get_logical_exams(year: int = None, subject: str = None):
    """
    Get (search) logical exams for given parameters.
    """

    response = admin.get_logical_exams(year, subject)

    if not response.success:
        raise HTTPException(status_code=404, detail=const.Message.LOG_EXAMS_NOT_FOUND)

    return response


@router.post("/exams/{examId}", response_model=BaseResponse, response_model_exclude_none=True)
async def post_exam(examId: int, exam: Score):
    """
    Update existing exam
    """

    response = admin.update_exam(examId, exam)

    if not response.success:
        raise HTTPException(status_code=404, detail=const.Message.EXAM_NOT_FOUND.format(examId))

    return response


@router.post("/exercises/{exercisesId}", response_model=BaseResponse, response_model_exclude_none=True)
async def post_exercise(exercisesId: int, exercise: Score):
    """
    Update existing exercise
    """

    response = admin.update_exercise(exercisesId, exercise)

    if not response.success:
        raise HTTPException(status_code=404, detail=const.Message.EXERCISE_NOT_FOUND.format(exercisesId))

    return response


@router.post("/scan/save", response_model=ExamFullResponse, response_model_exclude_none=True)
async def post_scan_save(file: UploadFile = File(...)):
    """
    Save a scan (file)
    """
    return scanner.save_scan_wrapper(file)


@router.get("/logical-exams/export")
async def get_logical_exams_export(year: int, subject: str):
    """
    Get (search) logical exams for given parameters, and export them to xlsx.
    """
    response = await admin.get_logical_exams_export(year, subject)

    if response is None or not isinstance(response, str):
        raise HTTPException(status_code=404, detail="Logical exams export failed")

    return response


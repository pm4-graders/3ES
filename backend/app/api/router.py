from fastapi import APIRouter, HTTPException, UploadFile, File, FastAPI
from .schema import BaseResponse, ExamFullResponse, ExamFullListResponse, LogicalExamListResponse, Score
import core.admin as admin
import core.scanner as scanner
import util.constant as const
from fastapi.staticfiles import StaticFiles

router = APIRouter(
    prefix='/api'
)


@router.delete("/exams/{examId}", response_model=BaseResponse, response_model_exclude_none=True)
async def delete_exam(examId: int):
    """
    Delete existing exam
    """

    response = admin.delete_exam(examId)

    if not response.success:
        raise HTTPException(status_code=404, detail=const.Message.EXAM_NOT_FOUND.format(examId))

    return response


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

    return admin.get_exams(year, subject)


@router.get("/logical-exams", response_model=LogicalExamListResponse, response_model_exclude_none=True)
async def get_logical_exams(year: int = None, subject: str = None):
    """
    Get (search) logical exams for given parameters.
    """

    return admin.get_logical_exams(year, subject)


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
    path = await admin.get_logical_exams_export(year, subject)

    if path is None or not isinstance(path, str):
        raise HTTPException(status_code=404, detail="Logical exams export failed")

    response = {
        'success': True,
        'path': path
    }
    return response

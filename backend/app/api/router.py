from fastapi import APIRouter, HTTPException, File, UploadFile
from .schema import BaseResponse, ExamFullResponse, ExamListResponse, ExamTotalScore, ExerciseScore
import core.admin as admin
import core.scanner as scanner

router = APIRouter(
    prefix='/api'
)


@router.post("/scan/save")
async def post_scan_save(file: UploadFile = File(...)) -> ExamFullResponse:
    print("1")
    return scanner.save_scan(file)


@router.get("/exams/{examId}")
async def get_exam(examId: int) -> ExamFullResponse:
    """
    Get exam and all its relationships
    """

    response = admin.get_exam_full(examId)

    if not response.success:
        raise HTTPException(status_code=404, detail="Exam " + str(examId) + " not found.")

    return response


@router.post("/exams/{examId}")
async def post_exam(examId: int, exam: ExamTotalScore) -> BaseResponse:
    """
    Update existing exam
    """

    response = admin.update_exam(examId, exam)

    if not response.success:
        raise HTTPException(status_code=404, detail="Exam " + str(examId) + " not found.")

    return response


@router.get("/exams")
async def get_exams(year: int = None, subject: str = None) -> ExamListResponse:
    """
    Get (search) exams for given parameters.
    """

    response = admin.get_exams(year, subject)

    if not response.success:
        raise HTTPException(status_code=404, detail="Exams not found.")

    return response


@router.post("/exercises/{exercisesId}")
async def post_exercise(exercisesId: int, exercise: ExerciseScore) -> BaseResponse:
    """
    Update existing exercise
    """

    response = admin.update_exercise(exercisesId, exercise)

    if not response.success:
        raise HTTPException(status_code=404, detail="Exercise " + str(exercisesId) + " not found.")

    return response

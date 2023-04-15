from datetime import date
from pydantic import BaseModel
from typing import Optional


class BaseResponse(BaseModel):
    success: bool


class Candidate(BaseModel):
    id: int
    number: str
    date_of_birth: date


class Exam(BaseModel):
    id: int
    year: int
    subject: str
    total_score: float


class Exercise(BaseModel):
    id: int
    number: str
    score: float
    accuracy: float


class ExamFull(BaseModel):
    id: int
    year: int
    subject: str
    total_score: float
    candidate: Optional[Candidate]
    exercises: list[Exercise]


class ExamFullResponse(BaseResponse, BaseModel):
    exam: Optional[ExamFull]


class ExamListResponse(BaseResponse, BaseModel):
    exams: list[Exam]


class ExamTotalScore(BaseModel):
    total_score: float


class ExerciseScore(BaseModel):
    score: float

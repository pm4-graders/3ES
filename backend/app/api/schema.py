from datetime import date
from pydantic import BaseModel
from typing import Optional


class BaseResponse(BaseModel):
    success: bool
    message: Optional[str] = None


class Candidate(BaseModel):
    id: int
    number: str
    date_of_birth: date


class Exam(BaseModel):
    id: int
    year: int
    subject: str
    score: float
    confidence: float


class Exercise(BaseModel):
    id: int
    number: str
    score: float
    confidence: float


class ExamFull(BaseModel):
    id: int
    year: int
    subject: str
    score: float
    confidence: float
    candidate: Candidate
    exercises: list[Exercise]


class ExamFullListResponse(BaseResponse, BaseModel):
    exams: list[ExamFull]


class ExamFullResponse(BaseResponse, BaseModel):
    exam: Optional[ExamFull] = None


class Score(BaseModel):
    score: float

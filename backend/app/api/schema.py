from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional


class BaseResponse(BaseModel):
    success: bool
    message: Optional[list[str]] = None


class Candidate(BaseModel):
    id: int
    number: str
    date_of_birth: date
    created_at: datetime
    updated_at: Optional[datetime] = None


class Exam(BaseModel):
    id: int
    year: int
    subject: str
    score: float
    confidence: float
    created_at: datetime
    updated_at: Optional[datetime] = None


class Exercise(BaseModel):
    id: int
    number: str
    score: float
    confidence: float
    created_at: datetime
    updated_at: Optional[datetime] = None


class ExamFull(Exam):
    candidate: Candidate
    exercises: list[Exercise]


class ExamFullListResponse(BaseResponse):
    exams: list[ExamFull]


class ExamFullResponse(BaseResponse):
    exam: Optional[ExamFull] = None


class LogicalExam(BaseModel):
    year: int
    subject: str


class LogicalExamListResponse(BaseResponse):
    logical_exams: list[LogicalExam]


class Score(BaseModel):
    score: float

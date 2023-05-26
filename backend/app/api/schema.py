from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional, List


class BaseResponse(BaseModel):
    success: bool
    message: Optional[List[str]] = None


class Candidate(BaseModel):
    id: int
    number: str
    date_of_birth: date
    created_at: datetime
    updated_at: Optional[datetime] = None


class Exam(BaseModel):
    id: int
    number: str
    year: int
    subject: str
    score: float = None
    total_score: float = None
    confidence: float
    picture_path: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class Exercise(BaseModel):
    id: int
    number: str
    score: float = None
    total_score: float = None
    confidence: float
    created_at: datetime
    updated_at: Optional[datetime] = None


class ExamFull(Exam):
    candidate: Candidate
    exercises: List[Exercise]


class ExamFullListResponse(BaseResponse):
    exams: List[ExamFull]


class ExamFullResponse(BaseResponse):
    exam: Optional[ExamFull] = None
    path: Optional[str] = None


class LogicalExam(BaseModel):
    year: int
    subject: str


class LogicalExamListResponse(BaseResponse):
    logical_exams: List[LogicalExam]


class Score(BaseModel):
    score: float

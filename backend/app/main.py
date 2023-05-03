from fastapi import FastAPI
from api import router
from model import database, model
from fastapi.middleware.cors import CORSMiddleware




# run app
app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.router)

# run db
database.db.connect()
database.db.create_tables(model.get_models())

# dummy data to run
candidate = model.Candidate.create(number='1', date_of_birth='1990-01-01')
exam = model.Exam.create(year='2017', subject='Math', score=14.5, confidence=0.9, candidate=candidate)
model.Exercise.create(number='1', score=10, confidence=0.8, exam=exam)
model.Exercise.create(number='2', score=4.5, confidence=0.7, exam=exam)

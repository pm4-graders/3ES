from fastapi import FastAPI
from api import router
from model import model, database
from model.model import Candidate, Exam, Exercise

# run app
app = FastAPI()
app.include_router(router.router)

# run db
database.db.connect()
database.db.create_tables(model.get_models())

# dummy data to run
candidate = Candidate.create(number='1', date_of_birth='1990-01-01')
exam = Exam.create(year='2017', subject='Math', total_score=14.5, candidate=candidate)
Exercise.create(number='1', score=10, accuracy=0.8, exam=exam)
Exercise.create(number='2', score=4.5, accuracy=0.7, exam=exam)

from fastapi import FastAPI
from api import router
import model.database as db
import model.model as model

# run app
app = FastAPI()
app.include_router(router.router)

# run db
db.db.connect()
db.db.create_tables(model.get_models())

# dummy data to run
candidate = model.Candidate.create(number='1', date_of_birth='1990-01-01')
exam = model.Exam.create(year='2017', subject='Math', total_score=14.5, candidate=candidate)
model.Exercise.create(number='1', score=10, accuracy=0.8, exam=exam)
model.Exercise.create(number='2', score=4.5, accuracy=0.7, exam=exam)

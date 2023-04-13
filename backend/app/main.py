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

#Dummy data to run 
Candidate.create(number='1', date_of_birth='01.01.1990')
Exam.create(year='2017', subject='Math', total_score='12', candidate_id=1)
Exercise.create(number='1', score=20, accuracy=0.8, exam_id=1)
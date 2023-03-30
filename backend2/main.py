from fastapi import FastAPI
from db import *

app = FastAPI()

@app.get("/candidates")
async def function_get_candidates():
    return Candidate.get()

@app.post("/candidate/{name}")
async def post_candidate(name: str):
    return Candidate.create({name} )

@app.get("/exams")
async def get_exams():
    return Exam.get()

@app.post("/exams/{name}")
async def post_candidate(name: str):
    return Exam.create({name} )

@app.post("/exercises/{name}")
async def post_exercise(name: str):
    return Exercise.create({name} )

@app.get("/excercise")
async def get_exercise():
    return Exercise.get()


db.connect()
db.create_tables([Candidate, Exam, Exercise])

# 4. Start the API application (on command line)
# !uvicorn main:app --reload


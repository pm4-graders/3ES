import asyncio

from api.schema import BaseResponse, Candidate, Exam, ExamFull, ExamFullResponse, ExamFullListResponse, Exercise, LogicalExam, LogicalExamListResponse
import core.database_handler as db
import model.model as model
import util.constant as const
import pandas as pd
import numpy as np
import nest_asyncio
import os

EXCELDIR = "output/"

nest_asyncio.apply()
def build_exam_full(exam):
    """
    Build exam with all its relationships
    """

    # candidate
    candidate = db.read_candidate(exam[model.Exam.candidate.name])

    # exam
    exam_rs = ExamFull(
        id=exam[model.Exam.id.name],
        year=exam[model.Exam.year.name],
        subject=exam[model.Exam.subject.name],
        score=exam[model.Exam.score.name],
        confidence=exam[model.Exam.confidence.name],
        created_at=exam[model.Exam.created_at.name],
        updated_at=exam[model.Exam.updated_at.name],
        candidate=Candidate(
            id=candidate[model.Candidate.id.name],
            number=candidate[model.Candidate.number.name],
            date_of_birth=candidate[model.Candidate.date_of_birth.name],
            created_at=candidate[model.Candidate.created_at.name],
            updated_at=candidate[model.Candidate.updated_at.name]
        ),
        exercises=[]
    )

    # exercises
    for exercise in db.read_exercises_by_exam(exam[model.Exam.id.name]):
        exam_rs.exercises.append(exercise)

    return exam_rs


def get_exam_full(exam_id):
    """
    Get exam and all its relationships
    """

    # exam response
    exam_rs = None

    # exam
    exam = db.read_exam(exam_id)

    if exam is not None:
        exam_rs = build_exam_full(exam)

    # response
    if exam_rs:
        return ExamFullResponse(success=True, exam=exam_rs)
    else:
        return ExamFullResponse(success=False)


def get_exams(year, subject):
    """
    Get (search) exams for given parameters.
    """

    exams_rs = []

    for exam in db.read_exams(year, subject):
        exams_rs.append(build_exam_full(exam))

    return ExamFullListResponse(
        success=True if exams_rs else False,
        exams=exams_rs
    )


def get_logical_exams(year, subject):
    """
    Get (search) logical exams for given parameters.
    """

    logical_exams_rs = []

    for logical_exam in db.read_logical_exams(year, subject):
        logical_exams_rs.append(LogicalExam(
            year=logical_exam.year,
            subject=logical_exam.subject
        ))

    return LogicalExamListResponse(
        success=True if logical_exams_rs else False,
        logical_exams=logical_exams_rs
    )


def update_exam(exam_id, exam):
    """
    Update existing exam
    """

    return BaseResponse(success=db.update_exam(exam_id, exam, const.Exam.CONFIDENCE_MAX))


def update_exercise(exercise_id, exercise):
    """
    Update existing exercise
    """

    return BaseResponse(success=db.update_exercise(exercise_id, exercise, const.Exercise.CONFIDENCE_MAX))



async def get_logical_exams_export(year, subject):
    loop = asyncio.get_running_loop()
    exams = await loop.run_in_executor(None, get_exams, year, subject)

    exams = get_exams(year, subject)

    array_values = ["Candicate ID", "Candidate Number", "Candidate date of birth", "candidate number", "Exam ID", "Exam Score"]

    max_exercises = 0
    exercieses_number = len(exams.exams)

    for i in range(0, exercieses_number):
        if len(exams.exams[i].exercises)>max_exercises:
            max_exercises = len(exams.exams[i].exercises)
            print(max_exercises)

    for i in range(1, max_exercises + 1):
        array_values.append(f"Exercise {i} ID")
        print("Exercise " + str(i) + " ID")

    output_array = np.empty((len(exams.exams) + 1, len(array_values)), dtype=object)
    output_array[0, :] = array_values

    # Loop through the array and fill the subsequent rows
    for i, value in enumerate(exams.exams):
        output_array[i + 1, 0] = exams.exams[i].candidate.id
        output_array[i + 1, 1] = exams.exams[i].candidate.number
        output_array[i + 1, 2] = exams.exams[i].candidate.date_of_birth
        output_array[i + 1, 3] = exams.exams[i].candidate.number
        output_array[i + 1, 4] = exams.exams[i].id
        output_array[i + 1, 5] = exams.exams[i].score
        output_array[i + 1, 6:] = [exams.exams[i].exercises[j]['score'] for j in range(0, len(exams.exams[i].exercises))]

    df = pd.DataFrame(output_array)

    os.makedirs(EXCELDIR, exist_ok=True)
    file_path = os.path.join(EXCELDIR, f'{year}_{subject}.xlsx')

    with pd.ExcelWriter(file_path) as writer:
        df.to_excel(writer, sheet_name="Sheet_1", index=False, header=True)

    manipulate_excel(file_path, year, subject)
    return file_path


def manipulate_excel(excel, year, subject):
    df = pd.read_excel(excel)
    empty_df = pd.DataFrame(np.nan, index=range(6), columns=df.columns)

    # Find the first column name
    first_column = df.columns[0]

    # Concatenate the original DataFrame to the new DataFrame


    empty_df.iloc[0, 0] = "AP Gymnasium: " + str(year)
    empty_df.iloc[2, 0] = str(subject)
    empty_df.iloc[4, 0] = "Total:"
    empty_df.iloc[5, 0] = "Mittelwert:"
    df = pd.concat([empty_df, df], ignore_index=True)

    # the first row are numbers of the dataframe, so we need to skip it

    df.to_excel(excel, index=False)





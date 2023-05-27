import datetime
import random


class CVResult:
    def __init__(self, candidate, exam):
        self.candidate = candidate
        self.exam = exam


class Candidate:
    def __init__(self, number, date_of_birth):
        self.number = number if number is not None else random.randint(90000, 99999)  # temporary default
        self.date_of_birth = date_of_birth if date_of_birth is not None else datetime.datetime(datetime.date.today().year - 14, random.randint(1, 12), random.randint(1, 28))  # temporary default


class Exam:
    def __init__(self, number, year, subject, score, total_score, confidence, exercises):
        self.number = number if number is not None else random.randint(100, 999)  # temporary default
        self.year = year if year is not None else datetime.date.today().year  # temporary default
        self.subject = subject if subject is not None else "Mathematik 1"  # temporary default
        self.score = score
        self.total_score = total_score
        self.confidence = confidence
        self.exercises = exercises

    def calc_exercises_score(self):
        return sum(exercise.score if exercise.score is not None else 0 for exercise in self.exercises)

    def calc_exercises_total_score(self):
        return sum(exercise.total_score if exercise.total_score is not None else 0 for exercise in self.exercises)


class Exercise:
    def __init__(self, number, score, total_score, confidence):
        self.number = number
        self.score = score
        self.total_score = total_score
        self.confidence = confidence

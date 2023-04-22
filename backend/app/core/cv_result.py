class Candidate:
    def __init__(self, number, date_of_birth):
        self.number = number
        self.date_of_birth = date_of_birth


class CVResult:
    def __init__(self, candidate, exam):
        self.candidate = candidate
        self.exam = exam


class Exam:
    def __init__(self, year, subject, score, confidence, exercises):
        self.year = year
        self.subject = subject
        self.score = score
        self.confidence = confidence
        self.exercises = exercises

    def calc_exercises_score(self):
        return sum(exercise.score for exercise in self.exercises)


class Exercise:
    def __init__(self, number, score, confidence):
        self.number = number
        self.score = score
        self.confidence = confidence

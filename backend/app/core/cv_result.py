class CVResult:
    def __init__(self, candidate, exam):
        self.candidate = candidate
        self.exam = exam


class Candidate:
    def __init__(self, number, date_of_birth):
        self.number = number
        self.date_of_birth = date_of_birth


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
    def __init__(self, number, score, confidence, max_score):
        self.number = number
        self.score = score
        self.confidence = confidence
        self.max_score = max_score

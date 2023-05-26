class CVResult:
    def __init__(self, candidate, exam):
        self.candidate = candidate
        self.exam = exam


class Candidate:
    def __init__(self, number, date_of_birth):
        self.number = number
        self.date_of_birth = date_of_birth


class Exam:
    def __init__(self, number, year, subject, score, total_score, confidence, exercises):
        self.number = number
        self.year = year
        self.subject = subject
        self.score = score
        self.total_score = total_score
        self.confidence = confidence
        self.exercises = exercises

    def calc_exercises_score(self):
        return sum(exercise.score for exercise in self.exercises)

    def calc_exercises_total_score(self):
        return sum(exercise.total_score for exercise in self.exercises)


class Exercise:
    def __init__(self, number, score, total_score, confidence):
        self.number = number
        self.score = score
        self.total_score = total_score
        self.confidence = confidence

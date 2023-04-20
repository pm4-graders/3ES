class CVResult:
    def __init__(self, candidate, exam):
        self.candidate = candidate
        self.exam = exam


class Candidate:
    def __init__(self, number, date_of_birth):
        self.number = number
        self.date_of_birth = date_of_birth


class Exam:
    def __init__(self, year, subject, total_score, exercises):
        self.year = year
        self.subject = subject
        self.total_score = total_score
        self.exercises = exercises

    def calc_total_score(self):
        return sum(exercise.score for exercise in self.exercises)


class ExamExercise:
    def __init__(self, number, score, accuracy, max_score):
        self.number = number
        self.score = score
        self.max_score = max_score
        self.accuracy = accuracy

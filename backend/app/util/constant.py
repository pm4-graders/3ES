class Entity:
    CANDIDATE = "candidate"
    EXAM = "exam"
    EXAMS = "exams"
    EXERCISE = "exercise"
    EXERCISES = "exercises"


class Exercise:
    ACCURACY_MAX = 1


class Candidate:
    DATE_OF_BIRTH_PATTERN = "%d.%m.%Y"


class Message:
    CV_EXCEPTION = "Computer Vision: {0}"
    EXAM_EXISTS = "Exam already exists."
    EXAM_NOT_FOUND = "Exam {0} not found."
    EXAMS_NOT_FOUND = "Exams not found."
    EXERCISE_NOT_FOUND = "Exercise {0} not found."


class Validation:
    W_SCORE_EQ = "Warning: The total score of the exam is unequal to the sum of the scores of the associated exercises"

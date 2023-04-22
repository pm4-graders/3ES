class ModelField:
    ID = "id"


class Entity:
    EXAMS = "exams"
    EXERCISES = "exercises"


class Exam:
    CONFIDENCE_MAX = 1


class Exercise:
    CONFIDENCE_MAX = 1


class Candidate:
    DATE_OF_BIRTH_PATTERN = "%d.%m.%Y"


class Message:
    CV_EXCEPTION = "Computer Vision: {0}"
    EXAM_EXISTS = "Exam already exists."
    EXAM_NOT_FOUND = "Exam {0} not found."
    EXAMS_NOT_FOUND = "Exams not found."
    EXERCISE_NOT_FOUND = "Exercise {0} not found."


class Validation:
    W_SCORE_EQ = "Warning: The score of the exam is unequal to the sum of the scores of the associated exercises"

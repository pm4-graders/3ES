import core.cv_result as cv_res


def get_dummy_cv_result():
    """
    Create and return a cv result with dummy values.
    """

    import json

    json_data = '{"candidate":{"number":"CHSG-23.123","date_of_birth":"2010-01-01"},"exam":{"year":2023,' \
                '"subject":"ABC English","score":4.00,"confidence":0.91, "exercises":[{' \
                '"number":"1.a","score":2.75,"confidence":0.88,"max_score":3},{"number":"1.b","score":2.00,' \
                '"confidence":0.98,"max_score":1}]},"result_validated":true} '

    data_dict = json.loads(json_data)

    candidate_data = data_dict['candidate']
    candidate = cv_res.Candidate(candidate_data['number'], candidate_data['date_of_birth'])

    exam_data = data_dict['exam']
    exercises = []
    for exercise_data in exam_data['exercises']:
        exercise = cv_res.Exercise(exercise_data['number'], exercise_data['score'], exercise_data['confidence'],
                                   exercise_data['max_score'])
        exercises.append(exercise)

    exam = cv_res.Exam(exam_data['year'], exam_data['subject'], exam_data['score'], exam_data['confidence'], exercises)

    return cv_res.CVResult(candidate, exam, data_dict['result_validated'])
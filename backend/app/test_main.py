import datetime
import unittest
from fastapi.testclient import TestClient
from peewee import SqliteDatabase
from main import app
from api.schema import Score
import core.database_handler as db
import core.admin as admin
from model.model import Candidate, Exam, Exercise, get_models
import util.dummy as dummy

ID_NOT_EXISTING = 9999
YEAR_EXISTING = 2023
YEAR_NOT_EXISTING = 9999
SUBJECT_EXISTING = 'English'
SUBJECT_NOT_EXISTING = '9999'


class TestApiRouter(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

        self.db = SqliteDatabase(':memory:')
        self.db.connect()
        self.db.drop_tables([Exam, Exercise, Candidate])
        self.db.create_tables([Exam, Exercise, Candidate])

        self.db_candidate = Candidate.create(number='1', date_of_birth=datetime.date(2000, 1, 1))
        self.db_exam = Exam.create(year=YEAR_EXISTING, subject=SUBJECT_EXISTING, score=90, confidence=0.8, candidate=self.db_candidate)
        self.db_exercise1 = Exercise.create(number='1', score=9.0, confidence=0.8, exam=self.db_exam)
        self.db_exercise2 = Exercise.create(number='2', score=8.5, confidence=0.9, exam=self.db_exam)

    def test_get_exam(self):
        # Test retrieving an exam that exists
        exam_full_rs = self.client.get("/api/exams/1")
        assert exam_full_rs.status_code == 200

        # Test retrieving a not existing exam
        exam_full_rs = self.client.get("/api/exams/" + str(ID_NOT_EXISTING))
        assert exam_full_rs.status_code == 404

    def test_get_exams(self):
        # Test retrieving an exam that exists
        exams_full_rs = self.client.get("/api/exams")
        assert exams_full_rs.status_code == 200

        exams_full_rs = self.client.get("/api/exams?year" + str(YEAR_EXISTING) + "&subject=" + SUBJECT_EXISTING)
        assert exams_full_rs.status_code == 200

        # Test retrieving a not existing exam
        exams_full_rs = self.client.get("/api/exams?year" + str(YEAR_NOT_EXISTING) + "&subject=" + SUBJECT_NOT_EXISTING)
        assert exams_full_rs.status_code == 404

    def test_get_logical_exams(self):
        # Test retrieving an exam that exists
        logical_exams_rs = self.client.get("/api/logical-exams")
        assert logical_exams_rs.status_code == 200

        logical_exams_rs = self.client.get("/api/logical-exams?year" + str(YEAR_EXISTING) + "&subject=" + SUBJECT_EXISTING)
        assert logical_exams_rs.status_code == 200

        # Test retrieving a not existing exam
        logical_exams_rs = self.client.get("/api/logical-exams?year" + str(YEAR_NOT_EXISTING) + "&subject=" + SUBJECT_NOT_EXISTING)
        assert logical_exams_rs.status_code == 404

    def test_post_exam(self):
        json_score = {"score": 5.1}

        # Test retrieving an exam that exists
        base_rs = self.client.post("/api/exams/1", json=json_score)
        assert base_rs.status_code == 200

        # Test retrieving a not existing exam
        base_rs = self.client.post("/api/exams/" + str(ID_NOT_EXISTING), json=json_score)
        assert base_rs.status_code == 404

    def test_post_exercise(self):
        json_score = {"score": 5.1}

        # Test retrieving an exam that exists
        base_rs = self.client.post("/api/exercises/1", json=json_score)
        assert base_rs.status_code == 200

        # Test retrieving a not existing exam
        base_rs = self.client.post("/api/exercises/" + str(ID_NOT_EXISTING), json=json_score)
        assert base_rs.status_code == 404

    def test_router_scanner_save(self):
        file = {"file": ("dummy file content", "dummy_file.jpg")}

        response = self.client.post("/api/scan/save", files=file)
        assert response.status_code == 200


class TestCoreAdmin(unittest.TestCase):

    def setUp(self):
        self.db = SqliteDatabase(':memory:')
        self.db.connect()
        self.db.drop_tables([Exam, Exercise, Candidate])
        self.db.create_tables([Exam, Exercise, Candidate])

        self.db_candidate = Candidate.create(number='1', date_of_birth=datetime.date(2000, 1, 1))
        self.db_exam = Exam.create(year=YEAR_EXISTING, subject=SUBJECT_EXISTING, score=90, confidence=0.8, candidate=self.db_candidate)
        self.db_exercise1 = Exercise.create(number='1', score=9.0, confidence=0.8, exam=self.db_exam)
        self.db_exercise2 = Exercise.create(number='2', score=8.5, confidence=0.9, exam=self.db_exam)

    def tearDown(self):
        self.db.drop_tables([Exam, Exercise, Candidate])

    def test_build_exam_full(self):
        candidate = db.read_candidate(self.db_candidate.id)
        exam = db.read_exam(self.db_exam.id)
        exercises = db.read_exercises_by_exam(self.db_exam.id)

        exam_full = admin.build_exam_full(exam)
        self.assertEqual(exam_full.id, exam[Exam.id.name])
        self.assertEqual(exam_full.year, exam[Exam.year.name])
        self.assertEqual(exam_full.subject, exam[Exam.subject.name])
        self.assertEqual(exam_full.score, exam[Exam.score.name])
        self.assertEqual(exam_full.confidence, exam[Exam.confidence.name])
        self.assertEqual(exam_full.created_at, exam[Exam.created_at.name])
        self.assertEqual(exam_full.created_at, exam[Exam.created_at.name])
        self.assertEqual(exam_full.candidate.id, candidate[Candidate.id.name])
        self.assertEqual(exam_full.candidate.number, candidate[Candidate.number.name])
        self.assertEqual(exam_full.candidate.date_of_birth, candidate[Candidate.date_of_birth.name])
        self.assertEqual(exam_full.candidate.created_at, candidate[Candidate.created_at.name])
        self.assertEqual(exam_full.candidate.updated_at, candidate[Candidate.updated_at.name])
        self.assertEqual(len(exam_full.exercises), len(exercises))

    def test_get_exam_full(self):
        # Test retrieving an exam that exists
        exam_full_rs = admin.get_exam_full(self.db_exam.id)
        self.assertTrue(exam_full_rs.success)
        self.assertEqual(exam_full_rs.exam.id, self.db_exam.id)

        # Test retrieving a not existing exam
        exam_full_rs = admin.get_exam_full(ID_NOT_EXISTING)
        self.assertFalse(exam_full_rs.success)
        self.assertIsNone(exam_full_rs.exam)

    def test_get_exams(self):
        # Test retrieving exams that exist
        exams_full_rs = admin.get_exams(year=None, subject=None)
        self.assertTrue(exams_full_rs.success)
        self.assertTrue(exams_full_rs.exams)

        # Test retrieving not existing exams
        exams_full_rs = admin.get_exams(year=YEAR_NOT_EXISTING, subject=SUBJECT_NOT_EXISTING)
        self.assertFalse(exams_full_rs.success)
        self.assertFalse(exams_full_rs.exams)

    def test_get_logical_exams(self):
        # Test retrieving logical exams that exist
        logical_exams_rs = admin.get_logical_exams(year=None, subject=None)
        self.assertTrue(logical_exams_rs.success)
        self.assertTrue(logical_exams_rs.logical_exams)

        # Test retrieving not existing logical exams
        logical_exams_rs = admin.get_logical_exams(year=YEAR_NOT_EXISTING, subject=SUBJECT_NOT_EXISTING)
        self.assertFalse(logical_exams_rs.success)
        self.assertFalse(logical_exams_rs.logical_exams)

    def test_update_exam(self):
        score = Score(score=5.1)

        # Test updating an existing exam
        base_rs = admin.update_exam(self.db_exam.id, score)
        self.assertTrue(base_rs.success)

        # Test updating a not existing exam
        base_rs = admin.update_exam(ID_NOT_EXISTING, score)
        self.assertFalse(base_rs.success)

    def test_update_exercise(self):
        score = Score(score=5.1)

        # Test updating an existing exercise
        base_rs = admin.update_exercise(self.db_exam.id, score)
        self.assertTrue(base_rs.success)

        # Test updating a not existing exercise
        base_rs = admin.update_exercise(ID_NOT_EXISTING, score)
        self.assertFalse(base_rs.success)


class TestCoreDatabaseHandler(unittest.TestCase):

    def setUp(self):
        self.db = SqliteDatabase(':memory:')
        self.db.connect()
        self.db.drop_tables([Exam, Exercise, Candidate])
        self.db.create_tables([Exam, Exercise, Candidate])

        self.db_candidate = Candidate.create(number='1', date_of_birth=datetime.date(2000, 1, 1))
        self.db_exam = Exam.create(year=YEAR_EXISTING, subject=SUBJECT_EXISTING, score=90, confidence=0.8, candidate=self.db_candidate)
        self.db_exercise1 = Exercise.create(number='1', score=9.0, confidence=0.8, exam=self.db_exam)
        self.db_exercise2 = Exercise.create(number='2', score=8.5, confidence=0.9, exam=self.db_exam)
        self.db_exam_empty = Exam.create(year=YEAR_EXISTING, subject=SUBJECT_EXISTING, score=90,
                                         confidence=0.8, candidate=self.db_candidate)
        self.exam = {Exam.year.name: 2022, Exam.subject.name: SUBJECT_EXISTING, Exam.score.name: 8,
                     Exam.confidence.name: 0.9}
        self.exercise3 = {Exercise.number.name: '3', Exercise.score.name: 3, Exercise.confidence.name: 0.8}

    def tearDown(self):
        self.db.drop_tables([Exam, Exercise, Candidate])

    def test_insert_exam(self):
        # Test inserting a new exam for a candidate
        db_exam = db.insert_exam(self.exam, self.db_candidate)
        self.assertIsNotNone(db_exam)
        self.assertEqual(db_exam.year, self.exam[Exam.year.name])
        self.assertEqual(db_exam.subject, self.exam[Exam.subject.name])
        self.assertEqual(db_exam.score, self.exam[Exam.score.name])
        self.assertEqual(db_exam.confidence, self.exam[Exam.confidence.name])
        self.assertEqual(db_exam.candidate, self.db_candidate)

        # Test retrieving an existing exam for a candidate
        db_exam = db.insert_exam(self.exam, self.db_candidate)
        self.assertIsNone(db_exam)

    def test_insert_exercise(self):
        # Test inserting a new exercise for an exam
        db_exercise = db.insert_exercise(self.exercise3, self.db_exam)
        self.assertIsNotNone(db_exercise)
        self.assertEqual(db_exercise.number, self.exercise3[Exercise.number.name])
        self.assertEqual(db_exercise.score, self.exercise3[Exercise.score.name])
        self.assertEqual(db_exercise.confidence, self.exercise3[Exercise.confidence.name])
        self.assertEqual(db_exercise.exam, self.db_exam)

        # Test retrieving an existing exercise for an exam
        db_exercise = db.insert_exercise(self.exercise3, self.db_exam)
        self.assertIsNone(db_exercise)

    def test_insert_or_get_candidate(self):
        # Test inserting a new candidate
        candidate = {Candidate.number.name: '2', Candidate.date_of_birth.name: datetime.date(2001, 1, 1)}
        db_candidate = db.insert_or_get_candidate(candidate)
        self.assertIsNotNone(db_candidate)
        self.assertEqual(db_candidate.number, candidate[Candidate.number.name])
        self.assertEqual(db_candidate.date_of_birth, candidate[Candidate.date_of_birth.name])

        # Test retrieving an existing candidate
        db_candidate = db.insert_or_get_candidate(candidate)
        self.assertIsNotNone(db_candidate)
        self.assertEqual(db_candidate.number, candidate[Candidate.number.name])
        self.assertEqual(db_candidate.date_of_birth, candidate[Candidate.date_of_birth.name])

    def test_read_candidate(self):
        # Test reading a candidate that exists
        candidate = db.read_candidate(self.db_candidate.id)
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate[Candidate.number.name], self.db_candidate.number)
        self.assertEqual(candidate[Candidate.date_of_birth.name], self.db_candidate.date_of_birth)

        # Test retrieving a not existing candidate
        candidate = db.read_candidate(ID_NOT_EXISTING)
        self.assertIsNone(candidate)

    def test_read_exam(self):
        # Test reading an exam that exists
        exam = db.read_exam(self.db_exam.id)
        self.assertIsNotNone(exam)
        self.assertEqual(exam[Exam.year.name], self.db_exam.year)
        self.assertEqual(exam[Exam.subject.name], self.db_exam.subject)
        self.assertEqual(exam[Exam.score.name], self.db_exam.score)
        self.assertEqual(exam[Exam.confidence.name], self.db_exam.confidence)
        self.assertEqual(exam[Exam.candidate.name], self.db_exam.candidate.id)

        # Test retrieving a not existing exam
        exam = db.read_exam(ID_NOT_EXISTING)
        self.assertIsNone(exam)

    def test_read_exams(self):
        # Test reading exams that exist
        exams = db.read_exams(year=YEAR_EXISTING, subject=SUBJECT_EXISTING)
        self.assertTrue(exams)

        exams = db.read_exams(year=YEAR_EXISTING, subject=None)
        self.assertTrue(exams)

        exams = db.read_exams(year=None, subject=SUBJECT_EXISTING)
        self.assertTrue(exams)

        exams = db.read_exams(year=None, subject=None)
        self.assertTrue(exams)

        # Test retrieving not existing exams
        exams = db.read_exams(year=YEAR_NOT_EXISTING, subject=SUBJECT_NOT_EXISTING)
        self.assertFalse(exams)

        exams = db.read_exams(year=YEAR_NOT_EXISTING, subject=None)
        self.assertFalse(exams)

        exams = db.read_exams(year=None, subject=SUBJECT_NOT_EXISTING)
        self.assertFalse(exams)

    def test_read_exercises_by_exam(self):
        # Test reading exercises by exam that exist
        exercises = db.read_exercises_by_exam(self.db_exam.id)
        self.assertEqual(2, len(exercises))
        self.assertEqual(exercises[0][Exercise.number.name], self.db_exercise1.number)
        self.assertEqual(exercises[0][Exercise.score.name], self.db_exercise1.score)
        self.assertEqual(exercises[0][Exercise.confidence.name], self.db_exercise1.confidence)

        # Test reading empty exercises by exam that exist
        exercises = db.read_exercises_by_exam(self.db_exam_empty.id)
        self.assertFalse(exercises)

        # Test retrieving exercises by not existing exams
        exercises = db.read_exercises_by_exam(ID_NOT_EXISTING)
        self.assertFalse(exercises)

    def test_read_logical_exams(self):
        # Test reading logical exams that exist
        logical_exams = db.read_logical_exams(year=YEAR_EXISTING, subject=SUBJECT_EXISTING)
        self.assertTrue(logical_exams)

        logical_exams = db.read_logical_exams(year=YEAR_EXISTING, subject=None)
        self.assertTrue(logical_exams)

        logical_exams = db.read_logical_exams(year=None, subject=SUBJECT_EXISTING)
        self.assertTrue(logical_exams)

        logical_exams = db.read_logical_exams(year=None, subject=None)
        self.assertTrue(logical_exams)

        # Test retrieving not existing logical exams
        logical_exams = db.read_logical_exams(year=YEAR_NOT_EXISTING, subject=SUBJECT_NOT_EXISTING)
        self.assertFalse(logical_exams)

        logical_exams = db.read_logical_exams(year=YEAR_NOT_EXISTING, subject=None)
        self.assertFalse(logical_exams)

        logical_exams = db.read_logical_exams(year=None, subject=SUBJECT_NOT_EXISTING)
        self.assertFalse(logical_exams)

    def test_save_scan_db(self):
        cv_data = dummy.get_dummy_cv_result()
        exam_count = len(db.read_exams(year=None, subject=None))

        # Test inserting a new scan by comparing exam
        exam_id = db.save_scan_db(cv_data)
        exam_count += 1
        self.assertEqual(exam_id, exam_count)

        # Test failed inserting a new scan by checking exam because of exam already existing
        exam_id = db.save_scan_db(cv_data)
        self.assertIsNone(exam_id)

    def test_update_exam(self):
        score = Score(score=5.1)

        # Test updating an existing exam
        self.assertTrue(db.update_exam(self.db_exam.id, score, 1.0))
        exam = db.read_exam(self.db_exam.id)
        self.assertEqual(exam[Exam.score.name], 5.1)
        self.assertEqual(exam[Exam.confidence.name], 1.0)

        # Test updating a not existing exam
        self.assertFalse(db.update_exam(ID_NOT_EXISTING, score, 1.0))

    def test_update_exercise(self):
        score = Score(score=5.1)

        # Test updating an existing exercise
        self.assertTrue(db.update_exercise(self.db_exercise1.id, score, 1.0))
        exercises = db.read_exercises_by_exam(self.db_exam.id)
        self.assertEqual(exercises[0][Exercise.score.name], 5.1)
        self.assertEqual(exercises[0][Exercise.confidence.name], 1.0)

        # Test updating a not existing exercise
        self.assertFalse(db.update_exercise(ID_NOT_EXISTING, score, 1.0))


class TestModelModel(unittest.TestCase):

    def test_get_models(self):
        self.assertEqual(get_models(), [Candidate, Exam, Exercise])

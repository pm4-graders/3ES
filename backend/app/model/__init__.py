# Import modules and sub-packages
from . import db


# Define package-level functions
def init_db():
    """
    Initialize the database
    """
    db.database.connect()
    db.database.create_tables([db.Candidate, db.Exam, db.Exercise])

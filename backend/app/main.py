from backend.app import init_app
from api import router
from model import database, model
from fastapi import FastAPI

# init app modules
init_app()

# run app
app = FastAPI()
app.include_router(router.router)

# run db
database.db.connect()
database.db.create_tables(model.getModels())

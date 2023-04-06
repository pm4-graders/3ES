from app import init_app
from app.api import router
from app.model import database, model
from fastapi import FastAPI

# init app modules
init_app()

# run app
app = FastAPI()
app.include_router(router.router)

# run db
database.db.connect()
database.db.create_tables(model.get_models())

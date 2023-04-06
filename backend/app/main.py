from fastapi import FastAPI
from api import router
from model import model, database

# run app
app = FastAPI()
app.include_router(router.router)

# run db
database.db.connect()
database.db.create_tables(model.get_models())

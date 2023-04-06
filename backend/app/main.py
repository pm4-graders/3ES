from backend.app.api import router
from backend.app.model import database, model
from fastapi import FastAPI

# run app
app = FastAPI()
app.include_router(router.router)

# run db
database.db.connect()
database.db.create_tables(model.get_models())

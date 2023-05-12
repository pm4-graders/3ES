from fastapi import FastAPI
from api import router
from model import database, model
from fastapi.middleware.cors import CORSMiddleware

# run app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.router)

# run db
database.db.connect()
database.db.create_tables(model.get_models())

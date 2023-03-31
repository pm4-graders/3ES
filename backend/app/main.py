from fastapi import FastAPI
from api import router

app = FastAPI()
app.include_router(router.router)

# 4. Start the API application (on command line)
# !uvicorn main:app --reload


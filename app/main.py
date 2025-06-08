from fastapi import FastAPI
from app.api.v1.api import api_router
from app.db.session import engine
from app.models import consultant as models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pool Consultant Management System",
    description="An agentic system to manage pool consultants.",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Pool Consultant Management System API"} 
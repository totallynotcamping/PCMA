from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.consultant import Training, TrainingCreate, Opportunity, OpportunityCreate, Attendance
from app.crud import crud_operations, crud_consultant

router = APIRouter()

# Training Agent Endpoints
@router.post("/consultants/{consultant_id}/trainings/", response_model=Training)
def add_training_record(
    consultant_id: int,
    training: TrainingCreate,
    db: Session = Depends(get_db),
):
    consultant = crud_consultant.get_consultant(db, consultant_id)
    if not consultant:
        raise HTTPException(status_code=404, detail="Consultant not found")
    return crud_operations.create_training(db=db, consultant_id=consultant_id, training=training)

# Opportunity Agent Endpoints
@router.post("/consultants/{consultant_id}/opportunities/", response_model=Opportunity)
def add_opportunity_record(
    consultant_id: int,
    opportunity: OpportunityCreate,
    db: Session = Depends(get_db),
):
    consultant = crud_consultant.get_consultant(db, consultant_id)
    if not consultant:
        raise HTTPException(status_code=404, detail="Consultant not found")
    return crud_operations.create_opportunity(db=db, consultant_id=consultant_id, opportunity=opportunity)

# Attendance Agent Endpoints
@router.post("/attendance/upload", response_model=List[Attendance])
async def upload_attendance_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV.")
    
    contents = await file.read()
    csv_content = contents.decode('utf-8')
    
    # In a real app, you might want to do more validation here
    attendances = crud_operations.bulk_create_attendance_from_csv(db, csv_content)
    return attendances 
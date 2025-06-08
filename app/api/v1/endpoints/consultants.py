from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import os
import shutil

from app.db.session import get_db
from app.schemas.consultant import Consultant, ConsultantCreate, ConsultantStatusDashboard, Skill, Training, Opportunity, Attendance
from app.crud import crud_consultant, crud_operations
from app.services.resume_agent import ResumeAgent

router = APIRouter()

@router.post("/", response_model=Consultant)
def create_consultant(consultant: ConsultantCreate, db: Session = Depends(get_db)):
    db_consultant = crud_consultant.get_consultant_by_email(db, email=consultant.email)
    if db_consultant:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_consultant.create_consultant(db=db, consultant=consultant)

@router.get("/", response_model=List[Consultant])
def read_consultants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    consultants = crud_consultant.get_consultants(db, skip=skip, limit=limit)
    return consultants

@router.get("/{consultant_id}", response_model=Consultant)
def read_consultant(consultant_id: int, db: Session = Depends(get_db)):
    db_consultant = crud_consultant.get_consultant(db, consultant_id=consultant_id)
    if db_consultant is None:
        raise HTTPException(status_code=404, detail="Consultant not found")
    return db_consultant

@router.post("/{consultant_id}/resume", status_code=202)
def upload_resume(
    consultant_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Ensure consultant exists
    db_consultant = crud_consultant.get_consultant(db, consultant_id=consultant_id)
    if not db_consultant:
        raise HTTPException(status_code=404, detail="Consultant not found")

    # Save the file
    upload_dir = os.path.join("uploads", "resumes")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{consultant_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create a record in the database
    crud_operations.create_resume_record(db, consultant_id, file_path)

    # Trigger the ResumeAgent to process the file
    resume_agent = ResumeAgent(db)
    # In a real-world scenario, you'd likely run this as a background task
    resume_agent.extract_skills_from_resume(file_path, consultant_id)
    
    return {"message": "Resume uploaded and processing started."}


@router.get("/{consultant_id}/dashboard", response_model=ConsultantStatusDashboard)
def get_consultant_dashboard(consultant_id: int, db: Session = Depends(get_db)):
    consultant = crud_consultant.get_consultant(db, consultant_id=consultant_id)
    if not consultant:
        raise HTTPException(status_code=404, detail="Consultant not found")

    # Resume Status
    resume_status = "Pending"
    if consultant.resumes:
        latest_resume = sorted(consultant.resumes, key=lambda r: r.uploaded_at, reverse=True)[0]
        resume_status = latest_resume.status

    # Attendance Report
    total_meetings = len(consultant.attendance)
    attended_meetings = len([a for a in consultant.attendance if a.status == 'Completed'])
    attendance_report = f"{attended_meetings}/{total_meetings} meetings attended"

    # Opportunities Provided
    opportunities_provided = len(consultant.opportunities)

    # Training Progress
    training_progress = "Not Started"
    if consultant.trainings:
        # A simple logic: if any training is 'In Progress' or 'Completed'
        if any(t.status == 'Completed' for t in consultant.trainings):
            training_progress = "Completed"
        elif any(t.status == 'In Progress' for t in consultant.trainings):
            training_progress = "In Progress"

    return ConsultantStatusDashboard(
        resume_status=resume_status,
        attendance_report=attendance_report,
        opportunities_provided=opportunities_provided,
        training_progress=training_progress,
    ) 
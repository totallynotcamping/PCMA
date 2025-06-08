from sqlalchemy.orm import Session
from app.models.consultant import Resume, Training, Opportunity, Attendance, Consultant
from app.schemas.consultant import TrainingCreate, OpportunityCreate, AttendanceCreate
import csv
from io import StringIO

def create_resume_record(db: Session, consultant_id: int, file_path: str):
    # Mark old resumes as outdated, if any
    db.query(Resume).filter(Resume.consultant_id == consultant_id).update({"status": "Outdated"})
    
    db_resume = Resume(consultant_id=consultant_id, file_path=file_path, status="Updated")
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

def create_training(db: Session, consultant_id: int, training: TrainingCreate):
    db_training = Training(**training.dict(), consultant_id=consultant_id)
    db.add(db_training)
    db.commit()
    db.refresh(db_training)
    return db_training

def create_opportunity(db: Session, consultant_id: int, opportunity: OpportunityCreate):
    db_opportunity = Opportunity(**opportunity.dict(), consultant_id=consultant_id)
    db.add(db_opportunity)
    db.commit()
    db.refresh(db_opportunity)
    return db_opportunity

def bulk_create_attendance_from_csv(db: Session, csv_content: str):
    reader = csv.DictReader(StringIO(csv_content))
    attendances = []
    for row in reader:
        # Assuming CSV has columns 'email', 'meeting_date', 'status'
        consultant = db.query(Consultant).filter(Consultant.email == row['email']).first()
        if consultant:
            attendance_data = AttendanceCreate(meeting_date=row['meeting_date'], status=row['status'])
            db_attendance = Attendance(**attendance_data.dict(), consultant_id=consultant.id)
            db.add(db_attendance)
            attendances.append(db_attendance)
    db.commit()
    return attendances 
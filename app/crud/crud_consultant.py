from sqlalchemy.orm import Session
from app.models.consultant import Consultant, Skill
from app.schemas.consultant import ConsultantCreate, SkillCreate

def get_consultant(db: Session, consultant_id: int):
    return db.query(Consultant).filter(Consultant.id == consultant_id).first()

def get_consultant_by_email(db: Session, email: str):
    return db.query(Consultant).filter(Consultant.email == email).first()

def get_consultants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Consultant).offset(skip).limit(limit).all()

def create_consultant(db: Session, consultant: ConsultantCreate):
    db_consultant = Consultant(email=consultant.email, name=consultant.name, department=consultant.department)
    db.add(db_consultant)
    db.commit()
    db.refresh(db_consultant)
    return db_consultant

def get_or_create_skill(db: Session, skill: SkillCreate):
    db_skill = db.query(Skill).filter(Skill.name == skill.name).first()
    if db_skill:
        return db_skill
    db_skill = Skill(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

def add_skill_to_consultant(db: Session, consultant_id: int, skill: SkillCreate):
    consultant = get_consultant(db, consultant_id)
    if not consultant:
        return None
    
    db_skill = get_or_create_skill(db, skill)
    
    if db_skill not in consultant.skills:
        consultant.skills.append(db_skill)
        db.commit()
        db.refresh(consultant)
        
    return consultant 
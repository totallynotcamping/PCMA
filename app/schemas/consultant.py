from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date, datetime

# Skill Schemas
class SkillBase(BaseModel):
    name: str

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int

    class Config:
        from_attributes = True

# Training Schemas
class TrainingBase(BaseModel):
    course_name: str
    completed_date: date
    status: str

class TrainingCreate(TrainingBase):
    pass

class Training(TrainingBase):
    id: int
    consultant_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Opportunity Schemas
class OpportunityBase(BaseModel):
    opportunity_description: Optional[str] = None
    status: str

class OpportunityCreate(OpportunityBase):
    pass

class Opportunity(OpportunityBase):
    id: int
    consultant_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Attendance Schemas
class AttendanceBase(BaseModel):
    meeting_date: date
    status: str

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    id: int
    consultant_id: int
    created_at: datetime

    class Config:
        from_attributes = True
        
# Resume Schemas
class ResumeBase(BaseModel):
    file_path: str
    status: str

class Resume(ResumeBase):
    id: int
    consultant_id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True

# Consultant Schemas
class ConsultantBase(BaseModel):
    name: str
    email: EmailStr
    department: Optional[str] = None

class ConsultantCreate(ConsultantBase):
    pass

class Consultant(ConsultantBase):
    id: int
    created_at: datetime
    skills: List[Skill] = []
    trainings: List[Training] = []
    opportunities: List[Opportunity] = []
    attendance: List[Attendance] = []
    resumes: List[Resume] = []


    class Config:
        from_attributes = Trueclass ConsultantStatusDashboard(BaseModel):
    resume_status: str
    attendance_report: str
    opportunities_provided: int
    training_progress: str 


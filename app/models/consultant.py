from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Table,
    Date,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

consultant_skills = Table(
    "consultant_skills",
    Base.metadata,
    Column("consultant_id", Integer, ForeignKey("consultants.id"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id"), primary_key=True),
)

class Consultant(Base):
    __tablename__ = "consultants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    department = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    resumes = relationship("Resume", back_populates="consultant")
    skills = relationship("Skill", secondary=consultant_skills, back_populates="consultants")
    trainings = relationship("Training", back_populates="consultant")
    opportunities = relationship("Opportunity", back_populates="consultant")
    attendance = relationship("Attendance", back_populates="consultant")

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    consultant_id = Column(Integer, ForeignKey("consultants.id"), nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="Pending")

    consultant = relationship("Consultant", back_populates="resumes")

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    consultants = relationship(
        "Consultant", secondary=consultant_skills, back_populates="skills"
    )

class Training(Base):
    __tablename__ = "trainings"
    id = Column(Integer, primary_key=True, index=True)
    consultant_id = Column(Integer, ForeignKey("consultants.id"), nullable=False)
    course_name = Column(String, nullable=False)
    completed_date = Column(Date, nullable=False)
    status = Column(String, default="Not Started")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    consultant = relationship("Consultant", back_populates="trainings")

class Opportunity(Base):
    __tablename__ = "opportunities"
    id = Column(Integer, primary_key=True, index=True)
    consultant_id = Column(Integer, ForeignKey("consultants.id"), nullable=False)
    opportunity_description = Column(String)
    status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    consultant = relationship("Consultant", back_populates="opportunities")

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    consultant_id = Column(Integer, ForeignKey("consultants.id"), nullable=False)
    meeting_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    consultant = relationship("Consultant", back_populates="attendance") 
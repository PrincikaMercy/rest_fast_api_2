from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Candidate(Base):
    __tablename__ = "candidate"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String, index=True)
    experience_needed = Column(String, index=True)
    position = Column(String, index=True)
    required_skill_set = Column(String, index=True)


class JobApplication(Base):
    __tablename__ = "job_application"

    id = Column(Integer, primary_key=True, index=True)
    candidate_first_name = Column(String, index=True)
    candidate_last_name = Column(String, index=True)
    gender = Column(String, index=True)
    mobile_number = Column(String, index=True)
    email_id = Column(String, index=True)
    experience = Column(String, index=True)
    apply_position = Column(String, index=True)
    skill_set = Column(String, index=True)

    candidate_id = Column(Integer, ForeignKey("candidate.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))





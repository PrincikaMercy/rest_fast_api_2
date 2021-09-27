from typing import List, Optional

from pydantic import BaseModel


class JobsBase(BaseModel):
    id: int

    class Config:
        orm_mode = True


class JobsCreate(JobsBase):
    job_name: str
    experience_needed: str
    position: str
    required_skill_set: str

    class Config:
        orm_mode = True


class Jobs(JobsBase):
    id: int

    class Config:
        orm_mode = True


class CandidateBase(BaseModel):
    email: str

    class Config:
        orm_mode = True


class CandidateCreate(CandidateBase):
    password: str

    class Config:
        orm_mode = True


class Candidate(CandidateBase):
    id: int
    is_active: bool
    items: List[Jobs] = []

    class Config:
        orm_mode = True


class ApplyJobs(BaseModel):
    id: int

    class Config:
        orm_mode = True


class ApplyCreate(JobsBase):
    candidate_first_name: str
    candidate_last_name: str
    gender: str
    mobile_number: str
    email_id: str
    experience: str
    apply_position: str
    skill_set: str

    class Config:
        orm_mode = True


class ApplyUpdate(JobsBase):
    candidate_first_name: str
    candidate_last_name: str
    gender: str
    mobile_number: str
    email_id: str
    experience: str
    apply_position: str
    skill_set: str

    class Config:
        orm_mode = True

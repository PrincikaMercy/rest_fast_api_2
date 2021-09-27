from sqlalchemy.orm import Session

import models
import schemas


def get_candidate(db: Session, candidate_id: int):
    return db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()


def get_candidate_by_email(db: Session, email: str):
    return db.query(models.Candidate).filter(models.Candidate.email == email).first()


def get_candidate_all(db: Session):
    return db.query(models.Candidate).all()


def create_candidate(db: Session, candidate: schemas.CandidateCreate):
    fake_hashed_password = candidate.password
    db_user = models.Candidate(email=candidate.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_jobs(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).all()


def create_candidate_app(db: Session, candidate: schemas.ApplyCreate, candidate_id: int):
    db_item = models.JobApplication(**candidate.dict(), candidate_id=candidate_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_jobs(db: Session, candidate: schemas.JobsCreate):
    db_item = models.Job(**candidate.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_application_id(db: Session, candidate_id: int):
    return db.query(models.JobApplication).filter(models.JobApplication.candidate_id == candidate_id).first()






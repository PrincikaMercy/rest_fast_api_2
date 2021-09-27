from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/api/v2/docs",
              redoc_url="/api/v2/redocs",
              title="Job Portal",
              description="This portal for job seekers",
              version="2.0",
              openapi_url="/api/v2/openapi.json", )


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Dependency
def get_db(request: Request):
    return request.state.db


@app.get("/")
async def homepage():
    url = "http://127.0.0.1:8000/api/v2/docs"
    return RedirectResponse(url=url)


def get_db_req(request: Request):
    return request.state.db


# CANDITATE

@app.post("/candidate/", response_model=schemas.Candidate, tags=["CANDIDATE"])
def create_candidate(candidate: schemas.CandidateCreate, db: Session = Depends(get_db_req)):
    db_user = crud.get_candidate_by_email(db, email=candidate.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_candidate(db=db, candidate=candidate)


@app.get("/candidate/", response_model=List[schemas.Candidate], tags=["CANDIDATE"])
def get_candidate(db: Session = Depends(get_db_req)):
    users = crud.get_candidate_all(db)
    return users


@app.get("/candidate/{candidate_id}", response_model=schemas.Candidate, tags=["CANDIDATE"])
def get_candidate_by_id(candidate_id: int, db: Session = Depends(get_db_req)):
    db_user = crud.get_candidate(db, candidate_id=candidate_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# JOBS

@app.post("/jobs", response_model=schemas.Jobs, tags=["JOBS"])
def create_jobs(
        jobs: schemas.JobsCreate, db: Session = Depends(get_db_req)):
    return crud.create_jobs(db=db, candidate=jobs)


@app.get("/jobs/{job_id}", response_model=schemas.Jobs, tags=["JOBS"])
def get_job_by_id(job_id: int, db: Session = Depends(get_db_req)):
    jobs = crud.get_jobs(db, job_id)
    return jobs


@app.put("/jobs/", response_model=schemas.Jobs, tags=["JOBS"])
def update_job(candidate: schemas.JobsCreate, candidate_id: int, db: Session = Depends(get_db_req)):
    db_user = crud.get_candidate(db, candidate_id=candidate_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_candidate(db=db, candidate=candidate)


# APPLICATION

@app.post("/apply_job/", response_model=schemas.Jobs, tags=["APPLICATION"])
def create_application(
        candidate_id: int, candidate: schemas.ApplyCreate, db: Session = Depends(get_db_req)
):
    return crud.create_candidate_app(db=db, candidate=candidate, candidate_id=candidate_id)


@app.put("/apply_job/", response_model=schemas.ApplyJobs, tags=["APPLICATION"])
def put_application(candidate: schemas.ApplyCreate, candidate_id: int, db: Session = Depends(get_db_req)):
    db_user = crud.get_application_id(db, candidate_id=candidate_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_candidate(db=db, candidate=candidate)


@app.get("/apply_job/{candidate_id}/", response_model=schemas.ApplyJobs, tags=["APPLICATION"])
def get_application_id(candidate_id: int, db: Session = Depends(get_db_req)):
    jobs = crud.get_application_id(db, candidate_id)
    return jobs

from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import create_access_token, oauth2_scheme, verify_token

from app import models, schemas
from app.database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

fake_user = {"username": "firstuser", "password": "first_user_password"}


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if (
        form_data.username != fake_user["username"]
        or form_data.password != fake_user["password"]
    ):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tasks/create", response_model=schemas.TaskResponse, status_code=201)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    verify_token(token)
    current_time = datetime.utcnow()
    db_task = models.Task(
        datetime_to_do=task.datetime_to_do,
        task_info=task.task_info,
        created_at=current_time,
        updated_at=current_time,
    )
    with db as session:
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
    return db_task


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(
    task_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    verify_token(token)
    task = db.query(models.Task).where(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}/update", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    verify_token(token)

    db_task = db.query(models.Task).where(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.datetime_to_do:
        db_task.datetime_to_do = task.datetime_to_do
    if task.task_info:
        db_task.task_info = task.task_info
    db_task.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/tasks", response_model=list[schemas.TaskResponse])
def get_tasks_list(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    verify_token(token)
    tasks = db.query(models.Task).all()
    return tasks


@app.get("/")
def root():
    return {"message": "FastTODO service is running"}

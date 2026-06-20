from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.models import Base
from app import crud
from app.schemas import TaskCreate, TaskUpdate, TaskResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Tracker API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tasks(db, skip=skip, limit=limit)

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    updated = crud.update_task(db, task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

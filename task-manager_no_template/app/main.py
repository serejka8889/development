from datetime import date
from fastapi import FastAPI, HTTPException, Query
from app.database import get_db_connection
from app.models import Task, TaskCreate, TaskUpdate
from app.crud import create_task, get_task_by_id, list_tasks, update_task, delete_task

app = FastAPI()

@app.on_event("startup")
async def startup():
    with get_db_connection() as cur:
        cur.execute(""" CREATE TABLE IF NOT EXISTS tasks ( id SERIAL PRIMARY KEY, title VARCHAR(255), description TEXT NULL, created_at DATE DEFAULT CURRENT_DATE, due_date DATE NULL, completed BOOLEAN DEFAULT FALSE ); """)

@app.post("/tasks/")
async def create_new_task(task: TaskCreate):
    new_task = create_task(task)
    if new_task is None:
        raise HTTPException(status_code=500, detail="Не удалось сохранить задачу")
    return {"message": "Задача создана успешно.", "data": new_task}

@app.get("/tasks/{task_id}/")
async def retrieve_task(task_id: int):
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена.")
    return {"data": task}

@app.get("/tasks/")
async def list_all_tasks(
    skip: int = Query(default=0),
    limit: int = Query(default=10, le=100),
    due_date: date = None,
    completed: bool = None
):
    tasks = list_tasks(skip, limit, due_date=due_date, completed=completed)
    return {"data": tasks}

@app.put("/tasks/{task_id}/")
async def update_existing_task(task_id: int, updated_task: TaskUpdate):
    task = update_task(task_id, updated_task)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена.")
    return {"message": "Задача обновлена успешно.", "data": task}

@app.delete("/tasks/{task_id}/")
async def remove_task(task_id: int):
    deleted_task = delete_task(task_id)
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена.")
    return {"message": "Задача удалена успешно."}
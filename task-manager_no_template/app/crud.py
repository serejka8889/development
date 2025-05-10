from typing import Optional, List
from app.database import get_db_connection
from app.models import Task, TaskCreate, TaskUpdate
from datetime import date


def create_task(task_create: TaskCreate):
    with get_db_connection() as cur:
        insert_query = " INSERT INTO tasks (title, description, created_at, due_date, completed) VALUES (%s, %s, %s, %s, %s) RETURNING *;"
        values = (
            task_create.title,
            task_create.description,
            date.today(),
            task_create.due_date,
            task_create.completed,
        )
        cur.execute(insert_query, values)
        result = cur.fetchone()
        if result:
            return Task(
                id=result[0],
                title=result[1],
                description=result[2],
                created_at=result[3],
                due_date=result[4],
                completed=result[5]
            )
        return None

def get_task_by_id(task_id: int):
    with get_db_connection() as cur:
        sql_query = """ SELECT * FROM tasks WHERE id=%s """
        cur.execute(sql_query, (task_id,))
        result = cur.fetchone()
        if result:
            return Task(
                id=result[0],
                title=result[1],
                description=result[2],
                created_at=result[3],
                due_date=result[4],
                completed=result[5]
            )
        else:
            return None

def list_tasks(skip: int = 0, limit: int = 100, completed: Optional[bool] = None, due_date: Optional[date] = None) -> \
list[Task] | None:
    conditions = []
    args = []
    if completed is not None:
        conditions.append("completed=%s")
        args.append(completed)
    if due_date is not None:
        conditions.append("due_date=%s")
        args.append(due_date)

    where_clause = f"WHERE {' AND '.join(conditions)}" if len(conditions) > 0 else ''

    with get_db_connection() as cur:
        sql = f"SELECT * FROM tasks {where_clause} ORDER BY id ASC OFFSET %s LIMIT %s"
        cur.execute(sql, (*args, skip, limit))
        result = cur.fetchall()
        if result:
            return [
                Task(
                id=row[0],
                title=row[1],
                description=row[2],
                created_at=row[3],
                due_date=row[4],
                completed=row[5]
                ) for row in result
            ]
        else:
            return None

def update_task(task_id: int, task_update: TaskUpdate):
    updates = {}
    if task_update.title is not None:
        updates["title"] = task_update.title
    if task_update.description is not None:
        updates["description"] = task_update.description
    if task_update.due_date is not None:
        updates["due_date"] = task_update.due_date
    if task_update.completed is not None:
        updates["completed"] = task_update.completed

    set_clause = ", ".join([f"{key}=%s" for key in updates.keys()])
    values = tuple(updates.values()) + (task_id,)

    with get_db_connection() as cur:
        sql_query = f""" UPDATE tasks SET {set_clause} WHERE id=%s RETURNING * """
        cur.execute(sql_query, values)
        result = cur.fetchone()
        if result:
            return Task(
                id=result[0],
                title=result[1],
                description=result[2],
                created_at=result[3],
                due_date=result[4],
                completed=result[5]
            )
        else:
            return None


def delete_task(task_id: int):
    with get_db_connection() as cur:
        sql_query = """ DELETE FROM tasks WHERE id=%s RETURNING * """
        cur.execute(sql_query, (task_id,))
        result = cur.fetchone()
        if result:
            return Task(
                id=result[0],
                title=result[1],
                description=result[2],
                created_at=result[3],
                due_date=result[4],
                completed=result[5]
            )
        else:
            return None
"""Репозиторий для задач"""

from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["TaskRepository"]


class TaskRepository(Repository):
    """Реализация хранилища задач"""

    @collect_response
    async def create(self, cmd: models.CreateTaskCommand) -> models.Task:
        q = """
            INSERT INTO tasks(title, description, deadline, status)
            VALUES (%(title)s, %(description)s, %(deadline)s, %(status)s)
            RETURNING id, title, description, deadline, status
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.ReadTaskQuery) -> models.Task:
        q = """
            SELECT id, title, description, deadline, status
            FROM tasks WHERE id = %(id)s
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchone()

    @collect_response
    async def filter_tasks(self, query: models.FilterTasksQuery) -> List[models.Task]:
        conditions = []
        params = {}

        if query.deadline is not None:
            conditions.append("deadline = %(deadline)s")
            params['deadline'] = query.deadline

        if query.status is not None:
            conditions.append("status = %(status)s")
            params['status'] = query.status

        where_clause = " AND ".join(conditions) if conditions else ""

        q = f""" SELECT id, title, description, deadline, status FROM tasks {"WHERE " + where_clause if where_clause else ""} """

        print("Final Query:", q)
        print("Parameters:", params)

        async with get_connection() as cur:
            await cur.execute(q, params)
            return await cur.fetchall()

    @collect_response
    async def update(self, cmd: models.UpdateTaskCommand) -> models.Task:
        q = """
            UPDATE tasks SET
                title = %(title)s,
                description = %(description)s,
                deadline = %(deadline)s,
                status = %(status)s
            WHERE id = %(id)s
            RETURNING id, title, description, deadline, status
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: models.DeleteTaskCommand) -> models.Task:
        q = """
            DELETE FROM tasks
            WHERE id = %(id)s
            RETURNING id, title, description, deadline, status
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

"""Сервис для модуля задач"""
from typing import List

from app.internal.repository.postgresql import task
from app.internal.repository.repository import BaseRepository
from app.pkg import models
from app.pkg.models.exceptions.task import TaskNotFound
from app.pkg.models.exceptions.repository import EmptyResult

__all__ = ["TaskService"]


class TaskService:
    """Сервис для управления задачами."""

    #: TaskRepository: Реализация хранилища задач
    repository: task.TaskRepository

    def __init__(self, task_repository: BaseRepository):
        self.repository = task_repository

    async def create_task(self, cmd: models.CreateTaskCommand) -> models.Task:
        """Создать задачу"""
        return await self.repository.create(cmd=cmd)

    async def read_task(self, query: models.ReadTaskQuery) -> models.Task:
        """Прочитать задачу."""
        try:
            return await self.repository.read(query=query)
        except EmptyResult as e:
            raise TaskNotFound from e

    async def filter_tasks(self, query: models.FilterTasksQuery) -> List[models.Task]:
        """Прочитать задачи по фильтрам срок и статус"""
        try:
            return await self.repository.filter_tasks(query=query)
        except EmptyResult as e:
            raise TaskNotFound("Задач не найдено, согласно заданному запросу.") from e

    async def update_task(self, cmd: models.UpdateTaskCommand) -> models.Task:
        """Обновить задачу"""
        return await self.repository.update(cmd=cmd)

    async def delete_task(self, cmd: models.DeleteTaskCommand) -> models.Task:
        """Удалить задачу"""
        return await self.repository.delete(cmd=cmd)

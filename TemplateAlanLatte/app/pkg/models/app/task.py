"""Модель для модуля задач"""
from pydantic.fields import Field
from pydantic.types import PositiveInt
from datetime import date
from app.pkg.models.base import BaseModel
from typing import Optional

__all__ = [
    "Task",
    "CreateTaskCommand",     
    "ReadTaskQuery", 
    "FilterTasksQuery",        
    "UpdateTaskCommand",     
    "DeleteTaskCommand",     
]

class BaseTask(BaseModel):
    """Базовая модель для задач"""

class TaskFields:
    id: PositiveInt = Field(description="ID задачи", example=1)
    title: str = Field(description="Название задачи", example="Завершить отчет")
    description: str = Field(description="Описание задачи", example="Провести исследование фреймворка")
    deadline: date = Field(description="Срок выполнения", example=date(2025, 5, 12))
    status: bool = Field(description="Статус выполнения задачи", example="False")

class _Task(BaseTask):
    """Класс задачи для повторного использования общих полей"""
    title: str = TaskFields.title
    description: str = TaskFields.description
    deadline: date = TaskFields.deadline
    status: bool = TaskFields.status

    class Config:
        json_encoders = {
            date: lambda dt: dt.isoformat(),
        }

class Task(_Task):
    """Полная модель задачи с ID"""
    id: PositiveInt = TaskFields.id


# Модели CRUD
class CreateTaskCommand(_Task):
    """Команда для создания задачи"""
    pass

class UpdateTaskCommand(_Task):
    """Команда для обновления задачи"""
    id: PositiveInt = TaskFields.id
    title: Optional[str] = TaskFields.title
    description: Optional[str] = TaskFields.description
    deadline: Optional[date] = TaskFields.deadline
    status: Optional[bool] = TaskFields.status

class DeleteTaskCommand(BaseTask):
    """Команда для удаления задачи."""
    id: PositiveInt = TaskFields.id

# Модели для запросов
class ReadTaskQuery(BaseTask):
    """Запрос для чтения задачи по ID"""
    id: PositiveInt = TaskFields.id
    
class FilterTasksQuery(BaseTask):
    """Запрос для фильтра задач по сроку и статусу"""
    deadline: Optional[date] = None
    status: Optional[bool] = None

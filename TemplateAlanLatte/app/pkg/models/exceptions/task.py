"""Exceptions for a Task model."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "TaskNotFound",
    "DuplicateTaskTitle",
    "InvalidTaskStatus",
    "TaskAlreadyCompleted",
    "ParentTaskNotFound",
]


class TaskNotFound(BaseAPIException):
    message = "Task not found."
    status_code = status.HTTP_404_NOT_FOUND


class DuplicateTaskTitle(BaseAPIException):
    message = "A task with this title already exists."
    status_code = status.HTTP_409_CONFLICT


class InvalidTaskStatus(BaseAPIException):
    message = "The provided task status is invalid or unsupported."
    status_code = status.HTTP_400_BAD_REQUEST


class TaskAlreadyCompleted(BaseAPIException):
    message = "This task has already been completed."
    status_code = status.HTTP_409_CONFLICT


class ParentTaskNotFound(BaseAPIException):
    message = "Parent task not found."
    status_code = status.HTTP_404_NOT_FOUND


__constrains__ = {
    "tasks_title_key": DuplicateTaskTitle,
}
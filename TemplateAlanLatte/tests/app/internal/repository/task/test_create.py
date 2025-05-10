"""Module for testing create task command."""

import asyncio

import pytest
from pydantic.error_wrappers import ValidationError

from app.internal.repository.postgresql.task import TaskRepository
from app.pkg import models
from app.pkg.models.exceptions.task import (
    TaskNotFound,
    DuplicateTaskTitle,
    TaskAlreadyCompleted,
    ParentTaskNotFound,
)


@pytest.mark.postgresql
async def test_correct(task_repository: TaskRepository, create_model, user_inserter):
    result, _ = await user_inserter()
    cmd = await create_model(models.CreateTaskCommand, user_id=result.id)
    task = await task_repository.create(cmd=cmd)

    assert isinstance(task, models.Task)
    assert task == cmd.migrate(model=models.Task, extra_fields={"id": task.id})


@pytest.mark.postgresql
async def test_duplicate_task_title(
    task_repository: TaskRepository,
    create_model,
    user_inserter,
):
    result, _ = await user_inserter()
    cmd_1 = await create_model(
        models.CreateTaskCommand,
        user_id=result.id,
        title="Important Task",
        description="First important task",
    )
    cmd_2 = await create_model(
        models.CreateTaskCommand,
        user_id=result.id,
        title="Important Task",
        description="Second important task",
    )

    await task_repository.create(cmd=cmd_1)

    with pytest.raises(DuplicateTaskTitle):
        await task_repository.create(cmd=cmd_2)


@pytest.mark.postgresql
async def test_task_already_completed(
    task_repository: TaskRepository,
    create_model,
    user_inserter,
):
    result, _ = await user_inserter()
    cmd = await create_model(
        models.CreateTaskCommand,
        user_id=result.id,
        title="Completed Task",
        description="This task is already completed",
        status=True,
    )
    created_task = await task_repository.create(cmd=cmd)

    with pytest.raises(TaskAlreadyCompleted):
        await task_repository.update(models.UpdateTaskCommand(
            id=created_task.id,
            status=False
        ))


@pytest.mark.postgresql
async def test_parent_task_not_found(
    task_repository: TaskRepository,
    create_model,
    user_inserter,
):
    result, _ = await user_inserter()
    cmd = await create_model(
        models.CreateTaskCommand,
        user_id=result.id,
        parent_id=-1,
        title="Subtask",
        description="A subtask that depends on non-existing parent",
    )

    with pytest.raises(ParentTaskNotFound):
        await task_repository.create(cmd=cmd)


@pytest.mark.parametrize(
    "deadline",
    [
        "2023-01-01",
        "invalid_date_format",
        "",
    ],
)
async def test_deadline_validation(create_model, deadline: str):
    with pytest.raises(ValidationError):
        await create_model(
            models.CreateTaskCommand,
            deadline=deadline,
            title="Test Task",
            description="Test Task Description",
            user_id=1,
        )
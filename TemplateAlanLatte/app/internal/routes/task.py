"""Роуты для модуля задач"""
import datetime
from typing import List, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status, Query

from app.internal.pkg.middlewares.fake_auth import fake_check_token
from app.internal.pkg.middlewares.token_based_verification import (
    token_based_verification,
)
from app.internal.routes import task_router
from app.internal.services import Services
from app.internal.services.task import TaskService
from app.pkg import models
from app.internal.pkg.middlewares import fake_auth
from app.pkg.models.app.task import FilterTasksQuery


@task_router.get(
    "/",
    response_model=List[models.Task],
    status_code=status.HTTP_200_OK,
    description="Получить задачи по фильтрам срок и статус",
    dependencies=[Depends(token_based_verification)],
    #dependencies=[Depends(fake_check_token)],
)
@inject
async def read_filter_tasks(
    task_service: Services.task_service = Depends(Provide[Services.task_service]),
    deadline: Optional[str] = Query(None, alias="deadline"),
    status: Optional[bool] = Query(None, alias="status"),
):

    filters = FilterTasksQuery()

    if deadline is not None:
        filters.deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
    if status is not None:
        filters.status = status

    return await task_service.filter_tasks(filters)

@task_router.get(
    "/{task_id:int}/",
    response_model=models.Task,
    status_code=status.HTTP_200_OK,
    description="Читать конкретную задачу по её ID",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def read_task_by_id(
    task_id: int,
    task_service: TaskService = Depends(Provide[Services.task_service]),
):
    return await task_service.read_task(query=models.ReadTaskQuery(id=task_id))


@task_router.post(
    "/",
    response_model=models.Task,
    status_code=status.HTTP_201_CREATED,
    description="Создать новую задачу",
    #dependencies=[Depends(fake_check_token)],
    dependencies=[Depends(token_based_verification)],
)
@inject
async def create_task(
    cmd: models.CreateTaskCommand,
    task_service: TaskService = Depends(Provide[Services.task_service]),
):
    return await task_service.create_task(cmd=cmd)


@task_router.put(
    "/",
    response_model=models.Task,
    status_code=status.HTTP_200_OK,
    description="Обновить существующую задачу",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def update_task(
    cmd: models.UpdateTaskCommand,
    task_service: TaskService = Depends(Provide[Services.task_service]),
):
    return await task_service.update_task(cmd=cmd)


@task_router.delete(
    "/{task_id:int}/",
    response_model=models.Task,
    status_code=status.HTTP_200_OK,
    description="Удалить задачу по её ID",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(Provide[Services.task_service]),
):
    return await task_service.delete_task(cmd=models.DeleteTaskCommand(id=task_id))

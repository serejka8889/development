"""Service layer."""

from dependency_injector import containers, providers
from app.internal.repository import Repositories, postgresql
from app.internal.services.task import TaskService


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    repositories: postgresql.Repositories = providers.Container(
        Repositories.postgres,
    )  # type: ignore

    task_service = providers.Factory(
        TaskService,
        task_repository=repositories.task_repository,
    )

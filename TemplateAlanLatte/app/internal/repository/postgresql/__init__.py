"""All postgresql repositories are defined here."""

from dependency_injector import containers, providers
from app.internal.repository.postgresql.task import TaskRepository


class Repositories(containers.DeclarativeContainer):
    """Container for postgresql repositories."""

    task_repository = providers.Factory(TaskRepository)

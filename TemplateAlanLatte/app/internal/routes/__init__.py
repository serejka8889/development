"""Global point for collected routers. __routes__ is a :class:`.Routes`
instance that contains all routers in your application.

Examples:
    After declaring all routers, you need to register them in your application::

       # >>> from fastapi import FastAPI
       # >>> app = FastAPI()
       # >>> __routes__.register_routes(app=app)
"""

from fastapi import APIRouter

from app.pkg.models.core.routes import Routes
from app.pkg.models.exceptions import (
    task,
)

__all__ = [
    "__routes__",
    "task_router",
]

task_router = APIRouter(
    prefix="/tasks",
    tags=["Task"],
    responses={
        **task.TaskNotFound.generate_openapi(),
        **task.DuplicateTaskTitle.generate_openapi(),
        **task.InvalidTaskStatus.generate_openapi(),
        **task.TaskAlreadyCompleted.generate_openapi(),
        **task.ParentTaskNotFound.generate_openapi(),
    },
)


__routes__ = Routes(
    routers=(
        task_router,
    ),
)

# /internal/pkg/middlewares/fake_auth.py

from fastapi import Depends

async def fake_check_token():
    # Всегда разрешаем доступ
    return {}
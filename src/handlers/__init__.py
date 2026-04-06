from aiogram import Router

from src.handlers import admin, registration, text


def setup_routers() -> Router:
    root = Router()
    root.include_router(admin.router)
    root.include_router(registration.router)
    # root.include_router(menu.router)
    root.include_router(text.router)
    return root

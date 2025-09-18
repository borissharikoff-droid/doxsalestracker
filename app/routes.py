from __future__ import annotations
from aiogram import Router
from app.routers.project import router as project_router
from app.routers.sales_join import router as sales_join_router
from app.routers.sales import router as sales_router

router = Router()
router.include_router(project_router)
router.include_router(sales_join_router)
router.include_router(sales_router)

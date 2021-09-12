# -*- coding: utf-8 -*-
from fastapi import APIRouter

from hostthedocs.controller.core.home import router as home_router
from hostthedocs.controller.api.v1.endpoints.hmfd import router as hmfd_router

# Core routers
core_routers = APIRouter()
core_routers.include_router(home_router)

# API routers
api_routers = APIRouter(prefix="/api/v1")
api_routers.include_router(hmfd_router)

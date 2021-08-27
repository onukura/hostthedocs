# -*- coding: utf-8 -*-
from fastapi import APIRouter

from hostthedocs.controller.api.v1.endpoints import hmfd, latest

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(hmfd.router)
api_router.include_router(latest.router)
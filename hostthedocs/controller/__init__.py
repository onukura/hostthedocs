# -*- coding: utf-8 -*-
from fastapi import APIRouter

from hostthedocs.controller import home

base_router = APIRouter()
base_router.include_router(home.router)

# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from hostthedocs import getconfig, util
from hostthedocs.config import get_settings
from hostthedocs.config import get_settings
from hostthedocs.controller import base_router
from hostthedocs.controller.api.v1 import api_router
from hostthedocs.filekeeper import (
    delete_files,
    insert_link_to_latest,
    parse_docfiles,
    unpack_project,
)

settings = get_settings()

app = FastAPI()

app.mount("/static", StaticFiles(directory=settings.ROOT_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(settings.ROOT_DIR / "templates"))

app.include_router(base_router)
app.include_router(api_router)

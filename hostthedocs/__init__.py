# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from hostthedocs.config import get_settings
from hostthedocs.controller import core_routers, api_routers

settings = get_settings()

app = FastAPI()

app.mount("/static", StaticFiles(directory=settings.ROOT_DIR / "static"), name="static")
app.mount(
    "/docfiles",
    StaticFiles(directory=settings.ROOT_DIR / "static" / "docfiles"),
    name="docfiles",
)
templates = Jinja2Templates(directory=str(settings.ROOT_DIR / "templates"))

app.include_router(core_routers)
app.include_router(api_routers)

# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from hostthedocs.filekeeper import parse_docfiles, insert_link_to_latest
from hostthedocs.config import get_settings, Settings

router = APIRouter()




@router.get("/")
async def home(request: Request, settings: Settings = Depends(get_settings), response_class=HTMLResponse):
    projects = parse_docfiles(settings.DOCFILES_DIR, settings.DOCFILES_LINK_ROOT)
    insert_link_to_latest(projects)
    templates = Jinja2Templates(directory=str(settings.ROOT_DIR / "templates"))
    return templates.TemplateResponse("index.html", {"request": request, "projects": projects})

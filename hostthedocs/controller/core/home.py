# -*- coding: utf-8 -*-
import os
from typing import Optional

from fastapi import APIRouter, Depends, Request, Path
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from hostthedocs.config import get_settings, Settings
from hostthedocs.internal.filekeeper import parse_docfiles, insert_link_to_latest

router = APIRouter()


@router.get("/")
async def home(request: Request, settings: Settings = Depends(get_settings)):
    projects = parse_docfiles(settings.DOCFILES_DIR, settings.DOCFILES_LINK_ROOT)
    insert_link_to_latest(projects)
    templates = Jinja2Templates(directory=str(settings.ROOT_DIR / "templates"))
    return templates.TemplateResponse(
        "index.html", {"request": request, "projects": projects}
    )


@router.get("/{project}/latest")
def latest_root(project: str = Path(...), settings: Settings = Depends(get_settings)):
    return latest(project, "", settings)


@router.get("/{project}/latest/{path}")
def latest(
    project: str = Path(...),
    path: Optional[str] = None,
    settings: Settings = Depends(get_settings),
):
    parsed_docfiles = parse_docfiles(settings.DOCFILES_DIR, settings.DOCFILES_LINK_ROOT)
    proj_for_name = dict((p.name, p) for p in parsed_docfiles)
    if project not in proj_for_name:
        return "Project %s not found" % project, 404
    latestindex = proj_for_name[project].versions[-1].link
    if path:
        latestlink = "%s/%s" % (os.path.dirname(latestindex), path)
    else:
        latestlink = latestindex
    return RedirectResponse("/" + latestlink)

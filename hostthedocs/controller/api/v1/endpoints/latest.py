# -*- coding: utf-8 -*-
import os

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from hostthedocs.filekeeper import parse_docfiles
from hostthedocs.config import get_settings, Settings

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/<project>/latest/")
def latest_root(project):
    return latest(project, "")


@router.get("/<project>/latest/<path:path>")
def latest(project: str, path: str, settings: Settings = Depends(get_settings)):
    parsed_docfiles = parse_docfiles(settings.DOCFILES_DIR, settings.DOCFILES_LINK_ROOT)
    proj_for_name = dict((p["name"], p) for p in parsed_docfiles)
    if project not in proj_for_name:
        return "Project %s not found" % project, 404
    latestindex = proj_for_name[project]["versions"][-1]["link"]
    if path:
        latestlink = "%s/%s" % (os.path.dirname(latestindex), path)
    else:
        latestlink = latestindex
    return RedirectResponse("/" + latestlink)

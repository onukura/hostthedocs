# -*- coding: utf-8 -*-
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel

from hostthedocs.internal.filekeeper import unpack_project, delete_files
from hostthedocs.config import get_settings, Settings

router = APIRouter()


@router.post("/hmfd")
async def hmfd(
    filedata: Optional[UploadFile] = File(...),
    name: str = Form(...),
    version: str = Form(...),
    description: str = Form(...),
    settings: Settings = Depends(get_settings),
):
    if settings.READONLY:
        return HTTPException(status_code=403, detail="Readonly mode now")

    if not filedata:
        return HTTPException(
            status_code=400, detail="Request is missing a zip/tar file."
        )
    unpack_project(filedata, name, version, description, settings.DOCFILES_DIR)
    return {"success": True}


class DeleteRequest(BaseModel):
    name: str
    version: str
    entire_project: Optional[bool]


@router.delete("/hmfd")
async def hmfd(request: DeleteRequest, settings: Settings = Depends(get_settings)):
    if settings.READONLY:
        return HTTPException(status_code=403, detail="Readonly mode now")

    if settings.DISABLE_DELETE:
        return HTTPException(status_code=403, detail="Delete disabled")

    delete_files(
        request.name,
        request.version,
        settings.DOCFILES_DIR,
        request.entire_project,
    )

    return {"success": True}

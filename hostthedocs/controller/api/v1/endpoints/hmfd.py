# -*- coding: utf-8 -*-
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile
from pydantic import BaseModel

from hostthedocs.config import Settings, get_settings
from hostthedocs.internal.filekeeper import delete_files, unpack_project

router = APIRouter()


@router.post("/hmfd")
async def hmfd_post(
    filedata: Optional[UploadFile] = File(...),
    name: str = Form(...),
    version: str = Form(...),
    description: str = Form(...),
    settings: Settings = Depends(get_settings),
) -> Response:
    if settings.READONLY:
        raise HTTPException(status_code=403, detail="Readonly mode now")

    if not filedata:
        raise HTTPException(
            status_code=400, detail="Request is missing a zip/tar file."
        )
    unpack_project(filedata, name, version, description, settings.DOCFILES_DIR)
    return Response(status_code=200)


class DeleteRequest(BaseModel):
    name: str
    version: str
    entire_project: Optional[bool]


@router.delete("/hmfd")
async def hmfd_delete(
    request: DeleteRequest, settings: Settings = Depends(get_settings)
) -> Response:
    if settings.READONLY:
        raise HTTPException(status_code=403, detail="Readonly mode now")

    if settings.DISABLE_DELETE:
        raise HTTPException(status_code=403, detail="Delete disabled")

    delete_files(
        request.name,
        request.version,
        settings.DOCFILES_DIR,
        request.entire_project,
    )

    return Response(status_code=200)

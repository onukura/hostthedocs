# -*- coding: utf-8 -*-
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from hostthedocs.filekeeper import unpack_project, delete_files
from hostthedocs.config import get_settings, Settings

router = APIRouter()


@router.post("/hmfd")
async def hmfd(
    file: Optional[UploadFile] = File(...), settings: Settings = Depends(get_settings)
):
    if settings.READONLY:
        return HTTPException(status_code=403, detail="Readonly mode now")

    if not file:
        return HTTPException(
            status_code=400, detail="Request is missing a zip/tar file."
        )
    uploaded_file = file.read()
    unpack_project(uploaded_file, request.form, settings.DOCFILES_DIR)
    uploaded_file.close()
    return {"success": True}


@router.delete("/hmfd")
async def hmfd(settings: Settings = Depends(get_settings)):
    if settings.READONLY:
        return HTTPException(status_code=403, detail="Readonly mode now")

    if settings.DISABLE_DELETE:
        return HTTPException(status_code=403, detail="Delete disabled")

    delete_files(
        request.args["name"],
        request.args.get("version"),
        settings.DOCFILES_DIR,
        request.args.get("entire_project"),
    )

    return {"success": True}

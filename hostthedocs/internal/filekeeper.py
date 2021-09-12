# -*- coding: utf-8 -*-
import os
import pathlib
import shutil
import tarfile
import tempfile
import zipfile
from codecs import open
from typing import List, Optional

import natsort
from fastapi import UploadFile
from pydantic import BaseModel

DEFAULT_PROJECT_DESCRIPTION = "No project description"


class Version(BaseModel):
    version: str
    link: str


class Project(BaseModel):
    name: str
    versions: List[Version]
    description: str


def sort_by_version(x: Version):
    # See http://natsort.readthedocs.io/en/stable/examples.html
    return x.version.replace(".", "~") + "z"


def _is_valid_doc_version(folder: pathlib.Path):
    """
    Test if a version folder contains valid documentation.

    A version folder contains documentation if:
    - is a directory
    - contains an `index.html` file
    """
    if not folder.is_dir():
        return False
    if not (folder / "index.html").exists():
        return False

    return True


def _get_proj_dict(
    proj_dir: pathlib.Path, link_root: pathlib.Path
) -> Optional[Project]:
    """
    Lookup for the configuration of a project.

    The project configuration is a :class:`dict` with the following data:
    - "name": the name of the project
    - "description": the description of the project
    - "versions": the list of the versions of the documentation. For each
      version, there is a :class:`dict` with:
      - "version": name of the version
      - "link": the relative url of the version

    If no valid versions have been found, returns ``None``.
    """
    allpaths = list(proj_dir.glob("*"))
    versions = [
        Version(
            version=p.name, link=f"{link_root.name}/{proj_dir.name}/{p.name}/index.html"
        )
        for p in allpaths
        if _is_valid_doc_version(p)
    ]
    if len(versions) == 0:
        return None

    versions = natsort.natsorted(versions, key=sort_by_version)
    descr = DEFAULT_PROJECT_DESCRIPTION
    if "description.txt" in [a.name for a in allpaths]:
        dpath = proj_dir / "description.txt"
        with open(str(dpath), "r", encoding="utf-8") as f:
            descr = f.read().strip()
    return Project(name=proj_dir.name, versions=versions, description=descr)


def paths_sorted(paths: List[pathlib.Path]) -> List[pathlib.Path]:
    return sorted(paths, key=lambda x: x.name)


def parse_docfiles(
    docfiles_dir: pathlib.Path, link_root: pathlib.Path
) -> Optional[List[Project]]:
    """
    Create the list of the projects.

    The list of projects is computed by walking the `docfiles_dir` and
    searching for project paths (<project-name>/<version>/index.html)
    """
    if not docfiles_dir.exists():
        return None

    projects: List[Project] = []
    folders: List[pathlib.Path] = paths_sorted(
        [p for p in docfiles_dir.iterdir() if p.is_dir()]
    )
    for folder in folders:
        project = _get_proj_dict(folder, link_root)
        if project is not None:
            projects.append(project)

    return projects


def find_root_dir(root_dir: pathlib.Path, file_ext: str = ".html") -> pathlib.Path:
    """
    Determines the documentation root directory by searching the top-level index file.
    """
    root_index_files = sorted(
        list(root_dir.glob(f"**/index{file_ext}")),
        key=lambda filename: len(filename.__str__().split(os.sep)),
    )
    if len(root_index_files) == 0:
        raise FileNotFoundError("Failed to find root index file!")
    else:
        return pathlib.Path(root_index_files[0]).parent.absolute()


def unpack_project(
    uploaded_file: UploadFile,
    name: str,
    version: str,
    description: str,
    docfiles_dir: pathlib.Path,
) -> None:
    projdir = docfiles_dir / name
    verdir = projdir / version

    if not os.path.isdir(verdir):
        os.makedirs(verdir)

    # Overwrite project description only if a (non empty) new one has been
    # provided
    descr = description
    if len(descr) > 0:
        descrpath = projdir / "description.txt"
        with open(descrpath.__str__(), "w", encoding="utf-8") as f:
            f.write(descr)

    if uploaded_file.filename.endswith(".zip"):
        filename = uploaded_file.filename
        fileobj = uploaded_file.file
        temp_dir = pathlib.Path(tempfile.mkdtemp())

        with open(str(temp_dir / filename), "wb+") as f:
            shutil.copyfileobj(fileobj, f)

        extract_dir = temp_dir / "__extract"
        extract_dir.mkdir()
        with zipfile.ZipFile(str(temp_dir / filename)) as existing_zip:
            existing_zip.extractall(extract_dir.__str__())

        # Determine documentation root dir by finding top-level index file
        root_dir = find_root_dir(extract_dir)

        # Then, only move root directory to target dir
        shutil.rmtree(verdir)  # clear possibly existing target dir
        shutil.move(root_dir, verdir)  # only move documentation root dir

        if os.path.isdir(temp_dir):  # cleanup temporary directory (if it still exists)
            shutil.rmtree(temp_dir)

    return None


def delete_files(
    name: str, version: str, docfiles_dir, entire_project: Optional[bool] = False
):
    remove = os.path.join(docfiles_dir, name)
    if not entire_project:
        remove = os.path.join(remove, version)
    if os.path.exists(remove):
        shutil.rmtree(remove)


def _has_latest(versions: List[Version]):
    return any(v.version == "latest" for v in versions)


def insert_link_to_latest(projects: List[Project]):
    """For each project in ``projects``,
    will append a "latest" version that links to a certain location
    (should not be to static files).
    Will not add a "latest" version if it already exists.

    :param projects: Project dicts to mutate.
    :param template: String to turn into a link.
      Should have a ``%(project)s`` that will be replaced with the project name.
    """
    for p in projects:
        if _has_latest(p.versions):
            continue
        link = f"{p.name}/latest"
        p.versions.append(Version(version="latest", link=link))

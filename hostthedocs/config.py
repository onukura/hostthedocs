# -*- coding: utf-8 -*-
import pathlib
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.absolute()
    # You must use None for default values!
    # All string values can be set using environment variables (prefixed with 'HTD_'),
    # such as 'HTD_DOCFILES_DIR' corresponds to the `docfiles_dir` attribute.

    # The directory that will contain the docfiles (stored user documentaiton).
    # If you're letting Host the Docs care care of serving, just leave it default
    # and let it serve from hostthedocs/static/docfiles.
    # Otherwise, point it to a place where your webserver is configured to serve
    # static content from.
    DOCFILES_DIR: pathlib.Path = ROOT_DIR / "static" / "docfiles"

    # Will be pre-pended to the links of the project files.
    # For example, if docfiles_dir is '~/htd/hostthedocs/static/docfiles'
    # then docfiles_link_root should be 'static/docfiles'
    DOCFILES_LINK_ROOT: pathlib.Path = ROOT_DIR / "static" / "docfiles"

    # If defined, is placed in the footer.
    # if not defined, don't display copyright.
    # Probably you want to use something
    # like 'Copyright &copy; My Company 2014'
    # Supports HTML.
    COPYRIGHT: str = ""

    # Title of the homepage.
    TITLE: str = "Host the Docs Home"

    # Message in jumbotron.
    WELCOME: str = "Welcome to Host the Docs!"
    # Message below jumbotron.
    # Supports HTML.
    INTRO: str = """
        Browse all available documentation below.
        To add your docs, see
        <a href="https://github.com/rgalanakis/hostthedocs#working-with-host-the-docs">these instructions</a>."""

    # If True, do not allow anything to be done via /hmfd
    READONLY: bool = False

    # If true does not allow the delete of a project or a version
    # to be done via /hmfd
    # It however can be done using ssh or similar tools
    DISABLE_DELETE: bool = False

    # Max upload size in MB (float or int)
    # Default to 8, may need to be much larger if you have big docs.
    MAX_CONTENT_MB: int = 8

    class Config:
        arbitrary_types_allowed = True
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()

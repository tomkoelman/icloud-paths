from __future__ import annotations

import platform
from pathlib import Path


def _find_platform_path(paths: dict[str, list[Path]], error_msg: str) -> Path | None:
    system = platform.system()
    if system not in paths:
        raise OSError(error_msg)
    home = Path.home()
    try:
        for relative in paths[system]:
            full = home / relative
            if full.exists():
                return full
        return None
    except OSError:
        return None


def get_icloud_drive_path() -> Path | None:
    return _find_platform_path(
        {
            "Darwin": [
                Path("Library/Mobile Documents/com~apple~CloudDocs"),
                Path("Desktop/iCloud Drive (Archive)"),
            ],
            "Windows": [Path("iCloud Drive")],
        },
        "iCloud Drive is only available on macOS and Windows",
    )


def _get_icloud_subpath(name: str) -> Path | None:
    drive = get_icloud_drive_path()
    if drive:
        path = drive / name
        try:
            if path.exists():
                return path
        except OSError:
            return None
    return None


def get_icloud_desktop_path() -> Path | None:
    return _get_icloud_subpath("Desktop")


def get_icloud_documents_path() -> Path | None:
    return _get_icloud_subpath("Documents")


def get_icloud_downloads_path() -> Path | None:
    return _get_icloud_subpath("Downloads")


def get_icloud_photos_path() -> Path | None:
    return _find_platform_path(
        {
            "Darwin": [Path("Pictures/Photos Library.photoslibrary")],
            "Windows": [Path("Pictures/iCloud Photos")],
        },
        "iCloud Photos is only available on macOS and Windows",
    )


class _ICloudMeta(type):
    @property
    def drive(cls) -> Path | None:
        return get_icloud_drive_path()

    @property
    def desktop(cls) -> Path | None:
        return get_icloud_desktop_path()

    @property
    def documents(cls) -> Path | None:
        return get_icloud_documents_path()

    @property
    def downloads(cls) -> Path | None:
        return get_icloud_downloads_path()

    @property
    def photos(cls) -> Path | None:
        return get_icloud_photos_path()

    @property
    def available(cls) -> bool:
        return is_icloud_available()


class iCloud(metaclass=_ICloudMeta):
    """Singleton providing iCloud paths as class properties."""


def is_icloud_available() -> bool:
    try:
        return get_icloud_drive_path() is not None
    except OSError:
        return False

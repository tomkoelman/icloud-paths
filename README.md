# iCloud Paths

A Python module for accessing common iCloud paths on macOS and Windows.

## Installation

```bash
uv add icloud-paths
```

## Usage

### `iCloud` class

```python
from icloud_paths import iCloud

if iCloud.available:
    drive = iCloud.drive
    desktop = iCloud.desktop
    documents = iCloud.documents
    downloads = iCloud.downloads
    photos = iCloud.photos
```

### Standalone functions

```python
from icloud_paths import (
    get_icloud_drive_path,
    get_icloud_desktop_path,
    get_icloud_documents_path,
    get_icloud_downloads_path,
    get_icloud_photos_path,
    is_icloud_available,
)

if is_icloud_available():
    drive = get_icloud_drive_path()
    desktop = get_icloud_desktop_path()
    documents = get_icloud_documents_path()
```

## API

### `iCloud` class properties

- `iCloud.drive` - iCloud Drive path
- `iCloud.desktop` - iCloud Desktop path
- `iCloud.documents` - iCloud Documents path
- `iCloud.downloads` - iCloud Downloads path
- `iCloud.photos` - Photos Library path (macOS) or iCloud Photos folder (Windows)
- `iCloud.available` - `True` if iCloud is accessible

### Standalone functions

- `get_icloud_drive_path()` - Returns iCloud Drive path
- `get_icloud_desktop_path()` - Returns iCloud Desktop path
- `get_icloud_documents_path()` - Returns iCloud Documents path
- `get_icloud_downloads_path()` - Returns iCloud Downloads path
- `get_icloud_photos_path()` - Returns Photos Library path (macOS) or iCloud Photos folder (Windows)
- `is_icloud_available()` - Checks if iCloud is accessible

All paths return `None` if the path is not available, or raise `OSError` if not on macOS/Windows.

## Requirements

- Python 3.8+
- macOS or Windows with iCloud for Windows installed

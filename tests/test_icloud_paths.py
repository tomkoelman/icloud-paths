import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from icloud_paths import (
    get_icloud_drive_path,
    get_icloud_desktop_path,
    get_icloud_documents_path,
    get_icloud_downloads_path,
    get_icloud_photos_path,
    is_icloud_available,
)


class TestiCloudDirectories:
    def test_get_icloud_drive_path_not_supported_os(self):
        """Test that get_icloud_drive_path raises OSError on unsupported systems."""
        with patch("platform.system", return_value="Linux"):
            with pytest.raises(
                OSError, match="iCloud Drive is only available on macOS and Windows"
            ):
                get_icloud_drive_path()

    @patch("platform.system", return_value="Darwin")
    def test_get_icloud_drive_path_exists_macos(self, mock_system):
        primary_path = Path("Library/Mobile Documents/com~apple~CloudDocs")
        mock_icloud_drive = MagicMock(spec=Path)
        mock_icloud_drive.exists.return_value = True

        mock_home = MagicMock(spec=Path)
        mock_home.__truediv__.side_effect = lambda p: (
            mock_icloud_drive
            if p == primary_path
            else MagicMock(spec=Path, exists=lambda: False)
        )

        with patch("pathlib.Path.home", return_value=mock_home):
            result = get_icloud_drive_path()
            assert result == mock_icloud_drive

    @patch("platform.system", return_value="Windows")
    def test_get_icloud_drive_path_exists_windows(self, mock_system):
        windows_path = Path("iCloud Drive")
        mock_icloud_drive = MagicMock(spec=Path)
        mock_icloud_drive.exists.return_value = True

        mock_home = MagicMock(spec=Path)
        mock_home.__truediv__.side_effect = lambda p: (
            mock_icloud_drive
            if p == windows_path
            else MagicMock(spec=Path, exists=lambda: False)
        )

        with patch("pathlib.Path.home", return_value=mock_home):
            result = get_icloud_drive_path()
            assert result == mock_icloud_drive

    @patch("platform.system", return_value="Darwin")
    def test_get_icloud_drive_path_not_exists(self, mock_system):
        with patch("pathlib.Path.home") as mock_home:
            mock_home.return_value = Path("/Users/test")
            with patch("pathlib.Path.exists", return_value=False):
                result = get_icloud_drive_path()
                assert result is None

    @patch("platform.system", return_value="Darwin")
    def test_get_icloud_drive_path_permission_error(self, mock_system):
        with patch("pathlib.Path.home") as mock_home:
            mock_home.return_value = Path("/Users/test")
            with patch("pathlib.Path.exists", side_effect=PermissionError):
                result = get_icloud_drive_path()
                assert result is None

    @pytest.mark.parametrize(
        "func",
        [
            get_icloud_desktop_path,
            get_icloud_documents_path,
            get_icloud_downloads_path,
        ],
    )
    @patch("icloud_paths.get_icloud_drive_path")
    def test_get_icloud_subdirectory_path_exists(self, mock_get_drive, func):
        mock_drive = MagicMock(spec=Path)
        mock_subdir = MagicMock(spec=Path)
        mock_subdir.exists.return_value = True
        mock_drive.__truediv__.return_value = mock_subdir
        mock_get_drive.return_value = mock_drive

        result = func()
        assert result == mock_subdir

    @pytest.mark.parametrize(
        "func",
        [
            get_icloud_desktop_path,
            get_icloud_documents_path,
            get_icloud_downloads_path,
        ],
    )
    def test_get_icloud_subdirectory_path_not_supported_os(self, func):
        with patch("platform.system", return_value="Linux"):
            with pytest.raises(OSError):
                func()

    @patch("icloud_paths.get_icloud_drive_path")
    def test_get_icloud_desktop_path_no_drive(self, mock_get_drive):
        mock_get_drive.return_value = None

        result = get_icloud_desktop_path()
        assert result is None

    def test_get_icloud_photos_path_not_supported_os(self):
        with patch("platform.system", return_value="Linux"):
            with pytest.raises(
                OSError, match="iCloud Photos is only available on macOS and Windows"
            ):
                get_icloud_photos_path()

    @patch("platform.system", return_value="Darwin")
    def test_get_icloud_photos_path_exists_macos(self, mock_system):
        macos_path = Path("Pictures/Photos Library.photoslibrary")
        mock_photos_path = MagicMock(spec=Path)
        mock_photos_path.exists.return_value = True

        mock_home = MagicMock(spec=Path)
        mock_home.__truediv__.side_effect = lambda p: (
            mock_photos_path
            if p == macos_path
            else MagicMock(spec=Path, exists=lambda: False)
        )

        with patch("pathlib.Path.home", return_value=mock_home):
            result = get_icloud_photos_path()
            assert result == mock_photos_path

    @patch("platform.system", return_value="Windows")
    def test_get_icloud_photos_path_exists_windows(self, mock_system):
        windows_path = Path("Pictures/iCloud Photos")
        mock_photos_path = MagicMock(spec=Path)
        mock_photos_path.exists.return_value = True

        mock_home = MagicMock(spec=Path)
        mock_home.__truediv__.side_effect = lambda p: (
            mock_photos_path
            if p == windows_path
            else MagicMock(spec=Path, exists=lambda: False)
        )

        with patch("pathlib.Path.home", return_value=mock_home):
            result = get_icloud_photos_path()
            assert result == mock_photos_path

    @patch("platform.system", return_value="Darwin")
    def test_get_icloud_photos_path_not_exists(self, mock_system):
        with patch("pathlib.Path.home") as mock_home:
            mock_home.return_value = Path("/Users/test")
            with patch("pathlib.Path.exists", return_value=False):
                result = get_icloud_photos_path()
                assert result is None

    @patch("icloud_paths.get_icloud_drive_path")
    def test_is_icloud_available_true(self, mock_get_drive):
        mock_get_drive.return_value = Path(
            "/Users/test/Library/Mobile Documents/com~apple~CloudDocs"
        )

        result = is_icloud_available()
        assert result is True

    @patch("icloud_paths.get_icloud_drive_path")
    def test_is_icloud_available_false(self, mock_get_drive):
        mock_get_drive.return_value = None

        result = is_icloud_available()
        assert result is False

    @patch("icloud_paths.get_icloud_drive_path")
    def test_is_icloud_available_os_error(self, mock_get_drive):
        mock_get_drive.side_effect = OSError("Not macOS")

        result = is_icloud_available()
        assert result is False

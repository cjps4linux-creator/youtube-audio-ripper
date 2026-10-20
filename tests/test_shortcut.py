"""Unit tests for the Windows shortcut helpers.

Two scripts are covered:

``create_desktop_shortcut.py``
    Exposes ``create_simple_ico()`` and ``create_shortcut()``.  It imports
    ``win32com.client`` inside a ``try/except ImportError`` because pywin32 is
    an optional Windows-only dependency, and it *runs* ``create_shortcut()``
    plus a Desktop clean-up loop at import time.

``create_shortcut.py``
    Exposes ``create_windows_shortcut(...)`` and also writes a ``.url`` file
    to the Desktop at import time.

Because both modules execute code on import and both touch the user's real
Desktop, they are never imported directly.  The ``load_script`` fixture in
``conftest.py`` imports a *copy* placed under ``tmp_path`` with
``os.path.expanduser("~")`` redirected to a throw-away home directory, so the
real Desktop and the real repository stay untouched.  ``create_simple_ico()``
likewise writes into the temporary copy's directory rather than the repo.

``win32com.client.Dispatch`` is always replaced by a recording double, so no
real COM object is created and no real ``.lnk`` file is written.  No test
opens a GUI window or touches the network.
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Import safety
# ---------------------------------------------------------------------------


def test_create_desktop_shortcut_module_imports_cleanly(load_script):
    module = load_script("create_desktop_shortcut.py")
    assert hasattr(module, "create_simple_ico")
    assert hasattr(module, "create_shortcut")


def test_create_shortcut_module_imports_cleanly(load_script):
    module = load_script("create_shortcut.py")
    assert hasattr(module, "create_windows_shortcut")


def test_desktop_shortcut_module_imports_without_pywin32(load_script):
    """pywin32 is optional: the module must still import when it is absent."""
    module = load_script("create_desktop_shortcut.py", hide_pywin32=True)
    assert module.Dispatch is None


def test_desktop_shortcut_module_defines_expected_paths(load_script):
    module = load_script("create_desktop_shortcut.py")
    assert module.script_file.name == "rip_gui.py"
    assert module.shortcut_path.name == "YouTube Audio Ripper.lnk"
    assert module.icon_path.name == "app_icon.ico"


# ---------------------------------------------------------------------------
# create_simple_ico()
# ---------------------------------------------------------------------------


def test_create_simple_ico_returns_a_path(load_script):
    module = load_script("create_desktop_shortcut.py")
    result = module.create_simple_ico()
    assert isinstance(result, Path)
    assert result.exists()


def test_create_simple_ico_writes_a_file(load_script):
    module = load_script("create_desktop_shortcut.py")
    icon = module.create_simple_ico()
    assert icon.is_file()
    assert icon.stat().st_size > 0


def test_create_simple_ico_starts_with_ico_magic_bytes(load_script):
    module = load_script("create_desktop_shortcut.py")
    icon = module.create_simple_ico()
    data = icon.read_bytes()
    assert data[:4] == b"\x00\x00\x01\x00"


def test_create_simple_ico_has_a_valid_ico_header(load_script):
    """ICONDIR: reserved=0, type=1 (icon), count=1 image."""
    module = load_script("create_desktop_shortcut.py")
    icon = module.create_simple_ico()
    data = icon.read_bytes()

    reserved, icon_type, count = struct.unpack("<HHH", data[:6])
    assert reserved == 0
    assert icon_type == 1
    assert count == 1


def test_create_simple_ico_directory_entry_fields(load_script):
    """The ICONDIRENTRY declares a 16x16, 32-bit image at offset 22."""
    module = load_script("create_desktop_shortcut.py")
    icon = module.create_simple_ico()
    data = icon.read_bytes()

    width, height, _colors, _reserved, _planes, bits, size, offset = struct.unpack(
        "<BBBBHHII", data[6:22]
    )
    assert width == 16
    assert height == 16
    assert bits == 32
    assert offset == 22
    assert size == 48


def test_create_simple_ico_payload_is_truncated(load_script):
    """ACTUAL behaviour: the generated ICO is 6 bytes shorter than it claims.

    The ICONDIRENTRY advertises ``bytesInRes = 48`` at ``offset = 22`` (70
    bytes total) but only 64 bytes are written, so the icon image data is
    truncated.  The file still starts with the ICO magic bytes, which is why
    Windows usually tolerates it.
    """
    module = load_script("create_desktop_shortcut.py")
    icon = module.create_simple_ico()
    data = icon.read_bytes()

    _reserved, _type, _count = struct.unpack("<HHH", data[:6])
    _w, _h, _c, _r, _planes, _bits, size, offset = struct.unpack("<BBBBHHII", data[6:22])

    assert len(data) == 64
    assert offset + size == 70
    assert len(data) < offset + size


def test_create_simple_ico_is_deterministic(load_script):
    module = load_script("create_desktop_shortcut.py")
    first = module.create_simple_ico().read_bytes()
    second = module.create_simple_ico().read_bytes()
    assert first == second


def test_create_simple_ico_writes_inside_the_isolated_copy_not_the_repo(load_script):
    """The icon must not be written into the real repository."""
    module = load_script("create_desktop_shortcut.py")
    icon = module.create_simple_ico()
    assert REPO_ROOT not in icon.resolve().parents
    assert not (REPO_ROOT / "app_icon.ico").exists()


def test_create_simple_ico_overwrites_a_previous_icon(load_script):
    module = load_script("create_desktop_shortcut.py")
    icon = module.create_simple_ico()
    icon.write_bytes(b"stale")
    module.create_simple_ico()
    assert icon.read_bytes() != b"stale"


# ---------------------------------------------------------------------------
# create_shortcut() -- pywin32 dependent
# ---------------------------------------------------------------------------


def test_create_shortcut_without_pywin32_prints_hint_and_returns_none(load_script, capsys):
    module = load_script("create_desktop_shortcut.py", hide_pywin32=True)
    assert module.create_shortcut() is None
    out = capsys.readouterr().out
    assert "pywin32 is not installed" in out


def test_create_shortcut_uses_dispatch_and_saves_the_lnk(load_script):
    """The helper drives WScript.Shell.CreateShortCut and calls save().

    NOTE: the module also invokes ``create_shortcut()`` at import time, so
    the recorder has already seen one dispatch before the explicit call.
    """
    module = load_script("create_desktop_shortcut.py")
    recorder = module.dispatch_recorder

    # One call happened while the module was being imported.
    assert recorder.progids == ["WScript.Shell"]
    import_time_shortcut = recorder.shortcuts[0]
    assert import_time_shortcut.saved is True

    module.create_shortcut()

    assert recorder.progids == ["WScript.Shell", "WScript.Shell"]
    assert recorder.shells[-1].paths[-1].endswith("YouTube Audio Ripper.lnk")
    assert recorder.shortcuts[-1].saved is True


def test_create_shortcut_configures_the_target_and_arguments(load_script):
    module = load_script("create_desktop_shortcut.py")
    recorder = module.dispatch_recorder

    module.create_shortcut()

    shortcut = recorder.shortcuts[-1]
    assert shortcut.Targetpath.endswith("python.exe")
    assert shortcut.Arguments.strip('"') == str(module.script_file)
    assert shortcut.WorkingDirectory == str(module.app_dir)
    assert shortcut.Description == "YouTube Audio Ripper"
    assert shortcut.IconLocation.endswith(",0")


def test_create_shortcut_is_a_noop_without_pywin32(load_script):
    """Without pywin32 the function returns early and never dispatches."""
    module = load_script("create_desktop_shortcut.py", hide_pywin32=True)
    assert module.create_shortcut() is None
    assert module.dispatch_recorder is None


# ---------------------------------------------------------------------------
# create_shortcut.py -- create_windows_shortcut()
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("target", "expected_url"),
    [
        (r"C:\Apps\ripper.exe", "URL=file:///C:\\Apps\\ripper.exe"),
        ("ripper.exe", "URL=file:///ripper.exe"),
        (r"D:\Tools\a b.exe", "URL=file:///D:\\Tools\\a b.exe"),
    ],
)
def test_create_windows_shortcut_returns_internet_shortcut_content(load_script, target, expected_url):
    module = load_script("create_shortcut.py")
    content = module.create_windows_shortcut(target, "ignored.lnk")
    assert "[InternetShortcut]" in content
    assert expected_url in content


def test_create_windows_shortcut_sets_icon_metadata(load_script):
    module = load_script("create_shortcut.py")
    content = module.create_windows_shortcut(r"C:\Apps\ripper.exe", "ignored.lnk")
    assert "IconFile=" in content
    assert "IconIndex=0" in content


def test_create_windows_shortcut_accepts_a_custom_description(load_script):
    """The description argument is accepted (the .url body does not use it)."""
    module = load_script("create_shortcut.py")
    content = module.create_windows_shortcut(
        r"C:\Apps\ripper.exe", "ignored.lnk", description="Custom text"
    )
    assert isinstance(content, str)
    assert "[InternetShortcut]" in content


def test_create_windows_shortcut_does_not_touch_the_filesystem(load_script, tmp_path):
    """It only returns the file content; it writes nothing itself."""
    module = load_script("create_shortcut.py")
    shortcut_path = tmp_path / "should-not-exist.lnk"
    module.create_windows_shortcut(r"C:\Apps\ripper.exe", str(shortcut_path))
    assert not shortcut_path.exists()


# ---------------------------------------------------------------------------
# Import-time side effects stay inside the temporary directory
# ---------------------------------------------------------------------------


def test_importing_create_shortcut_does_not_write_to_the_real_desktop(load_script, real_home):
    """The module writes a .url on import -- but only inside tmp_path."""
    real_desktop = real_home / "Desktop"
    before = set(real_desktop.glob("YouTube*")) if real_desktop.is_dir() else set()

    module = load_script("create_shortcut.py")

    after = set(real_desktop.glob("YouTube*")) if real_desktop.is_dir() else set()
    assert after == before
    assert module.url_path.exists()
    assert module.url_path.parent != real_desktop


def test_importing_create_desktop_shortcut_removes_only_temporary_desktop_files(load_script, real_home):
    """The module unlinks Desktop/YouTube* on import -- only inside tmp_path."""
    real_desktop = real_home / "Desktop"
    before = set(real_desktop.glob("YouTube*")) if real_desktop.is_dir() else set()

    def seed(home):
        (home / "Desktop" / "YouTube Audio Ripper.lnk").write_text("old", encoding="utf-8")

    module = load_script("create_desktop_shortcut.py", prepare=seed)

    after = set(real_desktop.glob("YouTube*")) if real_desktop.is_dir() else set()
    assert after == before
    # The fake Desktop is the one that was cleaned, not the real one.
    assert module.desktop.parent != real_desktop
    assert module.desktop.is_dir()


@pytest.mark.skipif(
    not sys.platform.startswith("win"),
    reason="Windows-only path semantics",
)
def test_shortcut_path_uses_a_lnk_extension(load_script):
    module = load_script("create_desktop_shortcut.py")
    assert module.shortcut_path.suffix == ".lnk"

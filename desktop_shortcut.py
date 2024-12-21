import os
from pathlib import Path


class DesktopShortcut:
    """This class represents all the methods and attributes needed to make the desktop shortcut."""

    def __init__(self, ide_name: str, bin_dir: Path):
        self.shortcut_path: Path = Path(
            f"/home/{os.getlogin()}", "Desktop", f"{ide_name}.desktop"
        )
        self.ide_name: str = ide_name
        self.exec_path: Path = bin_dir / ide_name.lower()
        self.icon_path: Path = bin_dir / f"{ide_name.lower()}.svg"

    def create_linux_shortcut(self):
        content = f"""
[Desktop Entry]
Version=1.0
Type=Application
Name={self.ide_name}
Icon={self.icon_path}
Exec="{self.exec_path}" %f
Comment=IDE
Categories=Development;IDE;
Terminal=false
"""
        with open(self.shortcut_path, "w") as file:
            file.write(content)
        # Make the shortcut executable
        self.shortcut_path.chmod(0o755)

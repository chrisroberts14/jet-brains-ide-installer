import os
import argparse
import subprocess
from pathlib import Path

from jetbrains_ide_installer.file_operations import FileOperations
from jetbrains_ide_installer.desktop_shortcut import DesktopShortcut


def check_is_root() -> bool:
    """
    Checks the user is running this as root.

    :return:
    """
    if os.geteuid() != 0:
        return False
    return True


def get_args() -> argparse.Namespace:
    """
    Get the args.

    :return:
    """
    parser = argparse.ArgumentParser(
        prog="JetBrains IDE Installer",
        description="Script to install JetBrains IDEs on linux for the tar file",
        usage="python3 -m jetbrains_ide_installer -t <path to tar file> -i <install dir>",
    )
    parser.add_argument(
        "--tar_file", "-t", help="Path to the tar file", required=True, type=Path
    )
    parser.add_argument(
        "--install_dir",
        "-i",
        help="Path to the installation directory",
        default=Path("/bin"),
        type=Path,
    )
    return parser.parse_args()


def main() -> int:
    """
    Run the script.

    :return:
    """
    if not check_is_root():
        print("Run this script as root")
        return 1

    # Get the arguments
    args = get_args()

    file_ops = FileOperations(args.tar_file, args.install_dir)
    install_path = file_ops.install()
    file_ops.add_to_path()

    # Create desktop shortcut
    desktop_shortcut = DesktopShortcut(file_ops.ide_name, install_path / "bin")
    desktop_shortcut.create_linux_shortcut()

    # Launch the IDE shell script to initialise the IDE
    subprocess.run([install_path / "bin" / (file_ops.ide_name.lower() + ".sh")])
    return 0


if __name__ == "__main__":
    exit(main())

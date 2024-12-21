import os
import subprocess
from pathlib import Path
import argparse
from file_operations import FileOperations
from desktop_shortcut import DesktopShortcut


def main(args: argparse.Namespace) -> int:
    """
    Run the script.

    :return:
    """
    file_ops = FileOperations(args.tar_file, args.install_dir)
    install_path = file_ops.install()
    file_ops.add_to_path()
    # Create desktop shortcut
    desktop_shortcut = DesktopShortcut(file_ops.ide_name, install_path / "bin")
    desktop_shortcut.create_linux_shortcut()
    # Launch the IDE
    subprocess.run([install_path / "bin" / (file_ops.ide_name.lower() + ".sh")])
    return 0


if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Please run this script as root")
        exit(1)
    # Arguments parser
    parser = argparse.ArgumentParser(description="Install a JetBrains IDE")
    parser.add_argument(
        "--tar-file", help="Path to the tar file", required=True, type=Path
    )
    parser.add_argument(
        "--install-dir",
        help="Path to the installation directory",
        default=Path("/bin"),
        type=Path,
    )
    parsed_args = parser.parse_args()
    exit(main(parsed_args))

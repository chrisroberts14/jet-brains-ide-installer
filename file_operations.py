import os
from pathlib import Path
import tarfile
import shutil


class FileOperations:
    def __init__(self, tar_file: Path, install_dir: Path):
        self.tar_file: Path = tar_file
        self.install_dir: Path = install_dir
        self.ide_name: str = tar_file.stem.split("-")[0]
        self.install_dir_name: Path = Path(
            install_dir, tar_file.name.replace(".tar.gz", "")
        )

    def install(self) -> Path:
        """
        Install the tar file in the installation directory.

        :return Path: The installation directory
        """
        # Extract the tar file in the installation directory
        # Files are in the form of name.tar.gz
        with tarfile.open(self.tar_file, "r:gz") as tar:
            tar.extractall(self.install_dir)
        return self.install_dir_name

    def add_to_path(self) -> None:
        """
        Add the bin directory to the PATH.

        :return:
        """
        # Find the bin directory
        bin_dir = self.install_dir_name / "bin"
        # Do this by editing the .bashrc file
        bashrc = Path(f"/home/{os.getlogin()}", ".bashrc")
        bashrc_copy = bashrc.with_suffix(".bashrc.bak")
        shutil.copy(bashrc, bashrc_copy)
        with open(bashrc, "a") as bashrc:
            line_to_add = f"export PATH=$PATH:{bin_dir}\n"
            bashrc.write(line_to_add)

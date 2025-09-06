import os
import glob

from typing import List


def list_files(dir_path: str, full_path: bool = False) -> List[str]:
    """
    Lists all files in a specified directory.

    Args:
        dir_path (str): Path to the directory.
        full_path (bool): Whether to return full file paths.

    Returns:
        List[str]: List of files in the directory.
    """
    files = glob.glob(dir_path + "/*")

    if not full_path:
        files = [os.path.basename(file) for file in files]

    return files

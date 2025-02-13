"""Utility script to clean up temporary files and directories created during podcast generation.

This script should be used with caution when other instances of the main program are running.
"""

# WARNING: This script will clear out all the files that are not the final audio file.
# This may cause problems when one instance of the script is running while another
# instance is already running. Make sure to run this script only when no other
# instances are running. Or implement a locking mechanism to prevent deletion of
# files that are still being used.

import os

DIRS_TO_CLEAR: list[str] = [
    ".tmp",
]

def cleanup_directory(dir_path: str = None) -> None:
    """Cleanup the given directory by deleting all files and subdirectories.
    
    Does not delete the directory itself or the final audio file.
    Does not modify anything outside the specified directory.
    """
    # If no directory is specified, cleanup all directories in DIRS_TO_CLEAR
    if dir_path is None:
        for dir_name in DIRS_TO_CLEAR:
            cleanup_directory(dir_name)
        return

    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            cleanup_directory(item_path)

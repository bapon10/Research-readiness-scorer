import os
from utils.file_utils import list_files

def check_tests(repo_path):
    files = list_files(repo_path)

    for f in files:
        if "test" in os.path.basename(f).lower():
            return {"score": 1, "status": "present", "details": "Test files found"}

    return {"score": 0, "status": "missing", "details": "No tests found"}
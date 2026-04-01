from utils.file_utils import find_file

def check_license(repo_path):
    file = find_file(repo_path, ["LICENSE", "LICENSE.txt"])

    if file:
        return {"score": 1, "status": "present", "details": "License found"}
    return {"score": 0, "status": "missing", "details": "No license"}
import subprocess

def check_version(repo_path):
    try:
        tags = subprocess.check_output(
            ["git", "-C", repo_path, "tag"],
            stderr=subprocess.DEVNULL
        ).decode().strip()

        if tags:
            return {"score": 1, "status": "present", "details": "Git tags found"}
    except:
        pass

    return {"score": 0, "status": "missing", "details": "No versioning found"}
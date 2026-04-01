import os

def check_ci(repo_path):
    github_ci = os.path.join(repo_path, ".github", "workflows")
    gitlab_ci = os.path.join(repo_path, ".gitlab-ci.yml")

    if os.path.exists(github_ci) or os.path.exists(gitlab_ci):
        return {"score": 1, "status": "present", "details": "CI found"}

    return {"score": 0, "status": "missing", "details": "No CI config"}
from utils.file_utils import find_file, search_keyword_in_file

def check_readme(repo_path):
    file = find_file(repo_path, ["README.md", "README.txt"])

    if not file:
        return {"score": 0, "status": "missing", "details": "No README found"}

    has_keywords = search_keyword_in_file(file, ["install", "usage"])

    return {
        "score": 1 if has_keywords else 0.5,
        "status": "good" if has_keywords else "weak",
        "details": "README with usage info" if has_keywords else "README lacks details"
    }
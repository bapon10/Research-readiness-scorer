from utils.file_utils import find_file, search_keyword_in_file

def check_citation(repo_path):
    file = find_file(repo_path, ["CITATION.cff"])

    if file:
        return {"score": 1, "status": "present", "details": "Citation file found"}

    readme = find_file(repo_path, ["README.md"])
    if readme and search_keyword_in_file(readme, ["citation"]):
        return {"score": 0.5, "status": "partial", "details": "Mention in README"}

    return {"score": 0, "status": "missing", "details": "No citation info"}
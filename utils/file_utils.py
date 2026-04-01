import os

def find_file(repo_path, filenames):
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.lower() in [f.lower() for f in filenames]:
                return os.path.join(root, file)
    return None

def search_keyword_in_file(file_path, keywords):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().lower()
            return all(k.lower() in content for k in keywords)
    except:
        return False

def list_files(repo_path, extension=None):
    result = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if extension:
                if file.endswith(extension):
                    result.append(os.path.join(root, file))
            else:
                result.append(os.path.join(root, file))
    return result
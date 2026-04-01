import os
import shutil
import tempfile
from git import Repo

def load_repo(input_path):
    if input_path.startswith("http"):
        temp_dir = tempfile.mkdtemp()
        Repo.clone_from(input_path, temp_dir)
        return temp_dir
    elif os.path.exists(input_path):
        return input_path
    else:
        raise Exception("Invalid repo path or URL")
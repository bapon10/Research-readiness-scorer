import os
from utils.file_utils import find_file, list_files

def check_reproducibility(repo_path):
    """
    Enhanced reproducibility check scoring 0-100 points:
    - Environment/dependency files (requirements.txt, environment.yml, etc.): 40 points
    - Docker/container support: 30 points
    - Notebook/example scripts: 20 points
    - Data/config files: 10 points
    """
    score = 0
    details_list = []
    
    # Check for environment/dependency files
    env_files = {
        "requirements.txt": "Python pip",
        "environment.yml": "Conda",
        "Pipfile": "Pipenv",
        "pyproject.toml": "Poetry/Python",
        "package.json": "Node.js",
        "Gemfile": "Ruby",
        "Cargo.toml": "Rust",
        "go.mod": "Go",
        "mix.exs": "Elixir",
    }
    
    env_file_found = None
    for filename, description in env_files.items():
        file_path = find_file(repo_path, [filename])
        if file_path:
            env_file_found = description
            score += 40
            details_list.append(f"Environment file found ({description}): {filename}")
            break
    
    # Check for Docker
    docker_files = find_file(repo_path, ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"])
    if docker_files:
        score += 30
        details_list.append("Docker configuration found")
    
    # Check for notebooks and example scripts
    notebook_files = []
    example_files = []
    all_files = list_files(repo_path)
    
    for f in all_files:
        basename = os.path.basename(f).lower()
        if basename.endswith(".ipynb"):
            notebook_files.append(f)
        elif "example" in basename or "demo" in basename or "tutorial" in basename:
            if basename.endswith((".py", ".js", ".r", ".jl", ".sh")):
                example_files.append(f)
    
    if notebook_files:
        score += 15
        details_list.append(f"Jupyter notebooks found ({len(notebook_files)})")
    
    if example_files:
        score += 5
        details_list.append(f"Example/demo scripts found ({len(example_files)})")
    
    # Check for data/config files
    data_indicators = 0
    for f in all_files:
        basename = os.path.basename(f).lower()
        if any(basename.endswith(ext) for ext in [".csv", ".json", ".yaml", ".yml", ".toml", ".conf", ".config"]):
            data_indicators += 1
    
    if data_indicators > 0:
        score += 10
        details_list.append(f"Data/config files found ({data_indicators})")
    
    status = "excellent" if score >= 90 else "good" if score >= 70 else "fair" if score >= 50 else "poor"
    
    if score == 0:
        status = "missing"
        details = "No reproducibility configuration found"
    else:
        details = "; ".join(details_list)
    
    return {
        "score": min(score, 100),
        "status": status,
        "details": details
    }

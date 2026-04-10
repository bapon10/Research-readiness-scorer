import os
import re
from utils.file_utils import find_file, list_files

def check_maintainability(repo_path):
    """
    Maintainability check scoring 0-100 points:
    - CONTRIBUTING.md or contribution guidelines: 25 points
    - Code organization (consistent structure): 25 points
    - Type hints/documentation: 25 points
    - Issue/PR templates: 15 points
    - Community guidelines (CODE_OF_CONDUCT): 10 points
    """
    score = 0
    details_list = []
    
    # Check for contribution guidelines
    contrib_file = find_file(repo_path, ["CONTRIBUTING.md", "CONTRIBUTING.txt", "CONTRIBUTING.rst", "DEVELOPMENT.md"])
    if contrib_file:
        score += 25
        details_list.append("Contribution guidelines found")
    
    # Check code organization
    src_files = list_files(repo_path)
    has_organized_structure = False
    
    # Look for organized directory structure (src/, lib/, tests/, docs/, etc.)
    organized_dirs = ["src", "lib", "source", "tests", "test", "docs", "documentation", "examples"]
    for dir_name in organized_dirs:
        dir_path = os.path.join(repo_path, dir_name)
        if os.path.isdir(dir_path):
            has_organized_structure = True
            break
    
    if has_organized_structure:
        score += 20
        details_list.append("Code well organized (structured directories)")
    
    # Check for type hints and documentation
    type_hints_count = 0
    docstring_count = 0
    total_py_files = 0
    
    for f in src_files:
        if f.endswith(".py"):
            total_py_files += 1
            try:
                with open(f, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                    # Check for type hints
                    if "->" in content or ": int" in content or ": str" in content or ": bool" in content:
                        type_hints_count += 1
                    # Check for docstrings
                    if '"""' in content or "'''" in content:
                        docstring_count += 1
            except:
                pass
    
    if total_py_files > 0:
        hint_ratio = type_hints_count / total_py_files
        doc_ratio = docstring_count / total_py_files
        
        if hint_ratio >= 0.5 or doc_ratio >= 0.5:
            score += 25
            details_list.append(f"Code documentation found ({doc_ratio*100:.0f}% with docstrings)")
        elif hint_ratio > 0 or doc_ratio > 0:
            score += 15
            details_list.append("Some code documentation present")
    
    # Check for issue/PR templates
    github_dir = os.path.join(repo_path, ".github")
    templates_found = False
    if os.path.isdir(github_dir):
        for file in os.listdir(github_dir):
            if "issue" in file.lower() or "pull_request" in file.lower() or "template" in file.lower():
                templates_found = True
                break
    
    if templates_found:
        score += 15
        details_list.append("Issue/PR templates found")
    
    # Check for code of conduct
    coc_file = find_file(repo_path, ["CODE_OF_CONDUCT.md", "code_of_conduct.md", "CODE-OF-CONDUCT.md"])
    if coc_file:
        score += 10
        details_list.append("Code of Conduct found")
    
    status = "excellent" if score >= 90 else "good" if score >= 70 else "fair" if score >= 50 else "poor"
    
    if score == 0:
        status = "missing"
        details = "No maintainability indicators found"
    else:
        details = "; ".join(details_list)
    
    return {
        "score": min(score, 100),
        "status": status,
        "details": details
    }

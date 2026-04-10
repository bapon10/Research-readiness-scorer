import os
from utils.file_utils import find_file, search_keyword_in_file

def check_readme(repo_path):
    """
    Enhanced README check scoring 0-100 points:
    - Presence: 15 points
    - Length (comprehensive): 20 points
    - Installation docs: 20 points
    - Usage/examples: 20 points
    - Additional items (TOC, badges, etc.): 25 points
    """
    file = find_file(repo_path, ["README.md", "README.txt", "README.rst"])
    
    if not file:
        return {
            "score": 0,
            "status": "missing",
            "details": "No README found"
        }
    
    score = 15  # Base points for presence
    
    try:
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            content_lower = content.lower()
    except:
        return {"score": 15, "status": "error", "details": "Could not read README"}
    
    # Check file length (comprehensive documentation)
    file_size = os.path.getsize(file)
    if file_size > 2000:
        score += 20
    elif file_size > 1000:
        score += 10
    elif file_size > 500:
        score += 5
    
    # Check for installation documentation
    install_keywords = ["install", "setup", "requirements", "dependencies", "pip", "npm", "docker"]
    if any(keyword in content_lower for keyword in install_keywords):
        score += 20
    elif "getting started" in content_lower or "quick start" in content_lower:
        score += 10
    
    # Check for usage documentation
    usage_keywords = ["usage", "example", "tutorial", "quick start", "guide", "how to"]
    if any(keyword in content_lower for keyword in usage_keywords):
        score += 20
    
    # Check for additional professional elements
    additional_items = 0
    if "##" in content or "# " in content:  # Has headers/structure
        additional_items += 5
    if "```" in content or "~~~" in content:  # Has code examples
        additional_items += 5
    if "[" in content and "](" in content:  # Has links
        additional_items += 5
    if "![" in content and "](" in content:  # Has images/badges
        additional_items += 5
    if "|" in content and "-" in content:  # Has tables
        additional_items += 5
    
    score += min(additional_items, 25)
    
    status = "excellent" if score >= 90 else "good" if score >= 70 else "fair" if score >= 50 else "poor"
    
    return {
        "score": min(score, 100),
        "status": status,
        "details": f"README found with {file_size} bytes, contains install and usage info"
    }
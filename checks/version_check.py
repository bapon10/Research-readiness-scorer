import subprocess
import os
import re
from utils.file_utils import find_file, list_files

def check_version(repo_path):
    """
    Enhanced version check scoring 0-100 points:
    - Git tags with semantic versioning: 30 points
    - Version in setup.py/pyproject.toml/package.json/Cargo.toml: 30 points
    - Changelog/Release notes: 25 points
    - Version consistency across files: 15 points
    """
    score = 0
    details_list = []
    versions_found = []
    
    # Check git tags
    git_tags = []
    try:
        tags = subprocess.check_output(
            ["git", "-C", repo_path, "tag"],
            stderr=subprocess.DEVNULL
        ).decode().strip().split("\n")
        
        # Filter for semantic versioning tags (v1.0.0, 1.0.0, etc.)
        semver_pattern = r'^v?\d+\.\d+\.\d+(-[a-zA-Z0-9]+)*$'
        git_tags = [t for t in tags if t and re.match(semver_pattern, t)]
        
        if git_tags:
            score += 30
            latest_tag = sorted(git_tags, key=lambda x: tuple(map(int, x.lstrip('v').split('.')[-3:])))[-1]
            details_list.append(f"Git tags found (latest: {latest_tag})")
            versions_found.append(latest_tag)
    except:
        pass
    
    # Check version files
    version_markers = {
        "setup.py": r'version\s*=\s*["\']([^"\']+)',
        "pyproject.toml": r'version\s*=\s*["\']([^"\']+)',
        "package.json": r'"version"\s*:\s*"([^"]+)"',
        "Cargo.toml": r'version\s*=\s*"([^"]+)"',
        "mix.exs": r'def project.*?:version,\s*"([^"]+)"',
        "composer.json": r'"version"\s*:\s*"([^"]+)"',
    }
    
    version_file_count = 0
    for filename, pattern in version_markers.items():
        file_path = find_file(repo_path, [filename])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    match = re.search(pattern, content)
                    if match:
                        version = match.group(1)
                        versions_found.append(version)
                        version_file_count += 1
            except:
                pass
    
    if version_file_count > 0:
        score += 30
        details_list.append(f"Version found in {version_file_count} config file(s)")
    
    # Check for Changelog
    changelog_files = find_file(repo_path, ["CHANGELOG.md", "CHANGELOG.txt", "CHANGELOG", "CHANGES.md", "HISTORY.md", "RELEASES.md"])
    if changelog_files:
        score += 25
        details_list.append("Changelog/Release notes found")
    
    # Check version consistency
    unique_versions = set(v.lstrip('v') for v in versions_found)
    if len(unique_versions) == 1:
        score += 15
        details_list.append("Version consistent across files")
    elif len(unique_versions) > 1:
        score += 5
        details_list.append(f"Multiple versions found: {', '.join(unique_versions)}")
    
    status = "excellent" if score >= 90 else "good" if score >= 70 else "fair" if score >= 50 else "poor"
    
    if score == 0:
        status = "missing"
        details = "No versioning information found"
    else:
        details = "; ".join(details_list)
    
    return {
        "score": min(score, 100),
        "status": status,
        "details": details
    }
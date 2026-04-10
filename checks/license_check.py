import os
from utils.file_utils import find_file

# Common SPDX license identifiers
SPDX_LICENSES = {
    "MIT", "Apache-2.0", "GPL-3.0", "GPL-2.0", "BSD-3-Clause", "BSD-2-Clause",
    "ISC", "MPL-2.0", "AGPL-3.0", "LGPL-3.0", "LGPL-2.1", "CC0-1.0",
    "Unlicense", "EPL-2.0", "WTFPL", "Zlib", "LGPL-3.0-only"
}

def check_license(repo_path):
    """
    Enhanced license check scoring 0-100 points:
    - Valid license file found: 50 points
    - Recognized SPDX license: 30 points
    - License headers in source files: 20 points
    """
    score = 0
    details_list = []
    
    # Check for license file
    license_file = find_file(repo_path, ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"])
    
    if license_file:
        score += 50
        details_list.append("License file found")
        
        # Check if it contains recognized license text
        try:
            with open(license_file, "r", encoding="utf-8", errors="ignore") as f:
                license_text = f.read()
                
            # Check for SPDX identifier or common license names
            for spdx in SPDX_LICENSES:
                if spdx in license_text or spdx.replace("-", " ") in license_text:
                    score += 30
                    details_list.append(f"SPDX license recognized: {spdx}")
                    break
            else:
                # Check for generic license keywords
                if any(kw in license_text for kw in ["permission", "distribute", "modify", "license"]):
                    score += 15
                    details_list.append("Generic license text detected")
        except:
            pass
    
    # Check for license headers in source files
    src_extensions = [".py", ".js", ".java", ".cpp", ".c", ".go", ".rs", ".rb"]
    license_header_count = 0
    total_src_files = 0
    
    for root, dirs, files in os.walk(repo_path):
        # Skip hidden and cache directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            if any(file.endswith(ext) for ext in src_extensions):
                total_src_files += 1
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()[:30]  # Check first 30 lines
                        content = "".join(lines).lower()
                        if "license" in content or "copyright" in content or "spdx" in content:
                            license_header_count += 1
                except:
                    pass
    
    if total_src_files > 0:
        header_ratio = license_header_count / total_src_files
        if header_ratio >= 0.5:
            score += 20
            details_list.append(f"License headers in {license_header_count}/{total_src_files} files")
        elif header_ratio > 0.1:
            score += 10
            details_list.append(f"License headers in {header_ratio*100:.0f}% of files")
    
    status = "excellent" if score >= 90 else "good" if score >= 70 else "fair" if score >= 50 else "poor"
    
    if score == 0:
        status = "missing"
        details = "No license file found"
    else:
        details = "; ".join(details_list)
    
    return {
        "score": min(score, 100),
        "status": status,
        "details": details
    }
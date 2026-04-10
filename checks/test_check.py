import os
import re
from utils.file_utils import list_files

def check_tests(repo_path):
    """
    Enhanced test check scoring 0-100 points:
    - Test files exist: 25 points
    - Test framework detected (pytest, unittest, etc.): 25 points
    - Minimum test count (>= 5 tests): 25 points
    - Coverage config (pytest-cov, coverage.py, etc.): 25 points
    """
    score = 0
    details_list = []
    
    # Framework detection patterns
    frameworks = {
        "pytest": [r"pytest", r"py\.test"],
        "unittest": [r"unittest", r"TestCase"],
        "jest": [r"jest", r"\.test\.js"],
        "mocha": [r"mocha"],
        "jasmine": [r"jasmine"],
        "vitest": [r"vitest"],
        "rspec": [r"rspec"],
        "jUnit": [r"junit"],
        "karma": [r"karma"],
    }
    
    files = list_files(repo_path)
    test_files = []
    test_framework_found = None
    coverage_config_found = False
    test_count = 0
    
    # Find test files
    for f in files:
        basename = os.path.basename(f).lower()
        
        # Look for test files
        if "test" in basename or basename.startswith("test"):
            test_files.append(f)
            
            # Count test functions
            try:
                with open(f, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                    # Count test functions (def test_*, it(*, describe(*, etc.)
                    test_count += len(re.findall(r'(def test_|def test\(|it\s*\(|describe\s*\()', content))
                    
                    # Detect test frameworks
                    for framework, patterns in frameworks.items():
                        for pattern in patterns:
                            if re.search(pattern, content):
                                test_framework_found = framework
                                break
            except:
                pass
        
        # Look for coverage config files
        if "coverage" in basename or ".coveragerc" in basename:
            coverage_config_found = True
        if "pytest.ini" in basename or "setup.cfg" in basename:
            if coverage_config_found is False:
                try:
                    with open(f, "r", encoding="utf-8", errors="ignore") as file:
                        if "cov" in file.read():
                            coverage_config_found = True
                except:
                    pass
    
    # Scoring
    if test_files:
        score += 25
        details_list.append(f"Found {len(test_files)} test file(s)")
    
    if test_framework_found:
        score += 25
        details_list.append(f"Test framework detected: {test_framework_found}")
    
    if test_count >= 5:
        score += 25
        details_list.append(f"Found {test_count} test functions")
    elif test_count > 0:
        score += 15
        details_list.append(f"Found {test_count} test function(s)")
    
    if coverage_config_found:
        score += 25
        details_list.append("Coverage configuration found")
    
    status = "excellent" if score >= 90 else "good" if score >= 70 else "fair" if score >= 50 else "poor"
    
    if score == 0:
        status = "missing"
        details = "No tests found"
    else:
        details = "; ".join(details_list)
    
    return {
        "score": min(score, 100),
        "status": status,
        "details": details
    }
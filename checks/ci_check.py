import os
import re

def check_ci(repo_path):
    """
    Enhanced CI check scoring 0-100 points:
    - CI config exists (GitHub Actions, GitLab, Travis, CircleCI, etc.): 40 points
    - Coverage reporting configured: 30 points
    - Security/linting checks configured: 30 points
    """
    score = 0
    details_list = []
    ci_systems = []
    
    # Check for various CI systems
    ci_configs = {
        "GitHub Actions": [".github/workflows", ".github/workflows/*.yml", ".github/workflows/*.yaml"],
        "GitLab CI": [".gitlab-ci.yml"],
        "Travis CI": [".travis.yml"],
        "CircleCI": [".circleci/config.yml", ".circleci"],
        "AppVeyor": ["appveyor.yml"],
        "Jenkins": ["Jenkinsfile"],
        "Azure Pipelines": ["azure-pipelines.yml"],
        "CodeShip": ["codeship-steps.yml", "codeship-services.yml"],
    }
    
    for ci_name, paths in ci_configs.items():
        for path in paths:
            full_path = os.path.join(repo_path, path)
            if os.path.exists(full_path):
                ci_systems.append(ci_name)
                break
    
    if ci_systems:
        score += 40
        details_list.append(f"CI Systems found: {', '.join(set(ci_systems))}")
        
        # Check for coverage and linting in workflows
        coverage_found = False
        linting_found = False
        
        # Try to read workflow files to detect coverage/linting
        workflow_dir = os.path.join(repo_path, ".github/workflows")
        if os.path.exists(workflow_dir):
            for file in os.listdir(workflow_dir):
                if file.endswith((".yml", ".yaml")):
                    try:
                        with open(os.path.join(workflow_dir, file), "r", encoding="utf-8") as f:
                            content = f.read().lower()
                            if any(kw in content for kw in ["coverage", "codecov", "coveralls", "codeclimate"]):
                                coverage_found = True
                            if any(kw in content for kw in ["lint", "eslint", "pylint", "flake8", "mypy", "black", "isort"]):
                                linting_found = True
                    except:
                        pass
        
        if coverage_found:
            score += 30
            details_list.append("Coverage reporting configured")
        else:
            score += 10
            details_list.append("Coverage reporting not detected")
        
        if linting_found:
            score += 30
            details_list.append("Linting/code quality checks configured")
        else:
            score += 10
            details_list.append("Linting checks not detected")
    
    status = "excellent" if score >= 90 else "good" if score >= 70 else "fair" if score >= 50 else "poor"
    
    if score == 0:
        status = "missing"
        details = "No CI configuration found"
    else:
        details = "; ".join(details_list)
    
    return {
        "score": min(score, 100),
        "status": status,
        "details": details
    }
import sys
from utils.repo_loader import load_repo
from checks.readme_check import check_readme
from checks.license_check import check_license
from checks.test_check import check_tests
from checks.ci_check import check_ci
from checks.version_check import check_version
from checks.citation_check import check_citation
from weights import WEIGHTS
from report.json_report import generate_json
from report.html_report import generate_html


def compute_score(results):
    total = 0
    for key, value in results.items():
        total += value["score"] * WEIGHTS[key]
    return int(total)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scorer.py <repo_path_or_url>")
        return

    repo_input = sys.argv[1]
    repo_path = load_repo(repo_input)

    results = {
        "readme": check_readme(repo_path),
        "license": check_license(repo_path),
        "tests": check_tests(repo_path),
        "ci": check_ci(repo_path),
        "version": check_version(repo_path),
        "citation": check_citation(repo_path)
    }

    total_score = compute_score(results)

    generate_json(results, total_score)
    generate_html(results, total_score)

    print(f"Final Score: {total_score}/100")


if __name__ == "__main__":
    main()
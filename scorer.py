import sys
from utils.repo_loader import load_repo
from checks.readme_check import check_readme
from checks.license_check import check_license
from checks.test_check import check_tests
from checks.ci_check import check_ci
from checks.version_check import check_version
from checks.citation_check import check_citation
from checks.reproducibility_check import check_reproducibility
from checks.maintainability_check import check_maintainability
from weights import WEIGHTS
from report.json_report import generate_json
from report.html_report import generate_html


def compute_score(results):
    """
    Compute final score by normalizing each check to 0-100 range
    and applying weights.
    """
    total = 0
    for key, value in results.items():
        # Normalize score (it's already 0-100)
        normalized_score = value["score"] / 100.0
        weighted_score = normalized_score * WEIGHTS.get(key, 0)
        total += weighted_score
    
    return round(total, 2)


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
        "citation": check_citation(repo_path),
        "reproducibility": check_reproducibility(repo_path),
        "maintainability": check_maintainability(repo_path)
    }

    total_score = compute_score(results)

    generate_json(results, total_score)
    generate_html(results, total_score)

    print(f"\n{'='*60}")
    print(f"Research Readiness Score: {total_score}/100")
    print(f"{'='*60}\n")
    
    # Print detailed breakdown
    print("Detailed Breakdown:")
    print("-" * 60)
    for key, value in results.items():
        weighted_value = (value["score"] / 100.0) * WEIGHTS.get(key, 0)
        print(f"{key:20} | Score: {value['score']:6.1f}/100 | Weighted: {weighted_value:6.2f}/{WEIGHTS.get(key, 0)}")
    print("-" * 60)
    print(f"Reports generated: report.json, report.html")


if __name__ == "__main__":
    main()
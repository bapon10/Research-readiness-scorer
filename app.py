from flask import Flask, request, jsonify, render_template
import os
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

app = Flask(__name__)


def compute_score(results):
    """
    Compute final score by normalizing each check to 0-100 range
    and applying weights.
    """
    total = 0
    for key, value in results.items():
        normalized_score = value["score"] / 100.0
        weighted_score = normalized_score * WEIGHTS.get(key, 0)
        total += weighted_score
    return round(total, 2)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ui")
def ui():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    if not data or not data.get("repo"):
        return jsonify({"error": "Missing 'repo' field in request body"}), 400

    repo_input = data.get("repo")

    try:
        repo_path = load_repo(repo_input)
        results = {
            "readme":          check_readme(repo_path),
            "license":         check_license(repo_path),
            "tests":           check_tests(repo_path),
            "ci":              check_ci(repo_path),
            "version":         check_version(repo_path),
            "citation":        check_citation(repo_path),
            "reproducibility": check_reproducibility(repo_path),
            "maintainability": check_maintainability(repo_path),
        }
        score = compute_score(results)
        return jsonify({
            "score":        score,
            "total_weight": sum(WEIGHTS.values()),
            "results":      results,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
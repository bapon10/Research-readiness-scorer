from flask import Flask, request, jsonify, render_template
import os

from utils.repo_loader import load_repo
from checks.readme_check import check_readme
from checks.license_check import check_license
from checks.test_check import check_tests
from checks.ci_check import check_ci
from checks.version_check import check_version
from checks.citation_check import check_citation
from weights import WEIGHTS

app = Flask(__name__)


def compute_score(results):
    total = 0
    for key, value in results.items():
        total += value["score"] * WEIGHTS[key]
    return int(total)


@app.route("/")
def home():
    return "API Running"


@app.route("/ui")
def ui():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    repo_input = data.get("repo")

    try:
        repo_path = load_repo(repo_input)

        results = {
            "readme": check_readme(repo_path),
            "license": check_license(repo_path),
            "tests": check_tests(repo_path),
            "ci": check_ci(repo_path),
            "version": check_version(repo_path),
            "citation": check_citation(repo_path)
        }

        score = compute_score(results)

        return jsonify({
            "score": score,
            "results": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
import json
from datetime import datetime
from weights import WEIGHTS


def generate_json(results, total_score):
    """Generate a comprehensive JSON report with metadata."""
    
    # Calculate weighted scores for each category
    weighted_results = {}
    for key, value in results.items():
        normalized_score = value["score"] / 100.0
        weighted_score = normalized_score * WEIGHTS.get(key, 0)
        weighted_results[key] = {
            "raw_score": value["score"],
            "max_score": 100,
            "weight": WEIGHTS.get(key, 0),
            "weighted_score": weighted_score,
            "status": value["status"],
            "details": value["details"]
        }
    
    output = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "scorer_version": "2.0",
            "total_weight": sum(WEIGHTS.values())
        },
        "score": {
            "total": total_score,
            "max": 100,
            "percentage": (total_score / 100) * 100
        },
        "categories": weighted_results,
        "summary": {
            "total_categories": len(results),
            "passing_categories": sum(1 for v in results.values() if v["score"] >= 50),
            "excellent_categories": sum(1 for v in results.values() if v["status"] == "excellent"),
            "good_categories": sum(1 for v in results.values() if v["status"] == "good"),
            "fair_categories": sum(1 for v in results.values() if v["status"] == "fair"),
            "poor_categories": sum(1 for v in results.values() if v["status"] == "poor" or v["status"] == "missing")
        }
    }

    with open("report.json", "w") as f:
        json.dump(output, f, indent=4)
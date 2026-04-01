import json

def generate_json(results, total_score):
    output = {
        "score": total_score,
        "checks": results
    }

    with open("report.json", "w") as f:
        json.dump(output, f, indent=4)
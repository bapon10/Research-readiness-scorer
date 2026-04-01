def generate_html(results, total_score):
    html = f"""
    <html>
    <head><title>Report</title></head>
    <body>
        <h1>Score: {total_score}</h1>
        <table border="1">
            <tr><th>Check</th><th>Status</th><th>Score</th><th>Details</th></tr>
    """

    for key, value in results.items():
        html += f"""
        <tr>
            <td>{key}</td>
            <td>{value['status']}</td>
            <td>{value['score']}</td>
            <td>{value['details']}</td>
        </tr>
        """

    html += "</table></body></html>"

    with open("report.html", "w") as f:
        f.write(html)
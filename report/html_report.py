def generate_html(results, total_score):
    """Generate a comprehensive HTML report with styling."""
    
    # Color coded status
    status_colors = {
        "excellent": "#27ae60",  # Green
        "good": "#3498db",       # Blue
        "fair": "#f39c12",       # Orange
        "poor": "#e74c3c",       # Red
        "missing": "#95a5a6"     # Gray
    }
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Research Readiness Score Report</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            .score-display {{
                font-size: 72px;
                font-weight: bold;
                margin: 20px 0;
            }}
            .score-max {{
                font-size: 28px;
                opacity: 0.8;
            }}
            .content {{
                padding: 40px;
            }}
            .checks-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-top: 30px;
            }}
            .check-card {{
                border: 2px solid #ecf0f1;
                border-radius: 8px;
                padding: 20px;
                transition: all 0.3s ease;
            }}
            .check-card:hover {{
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                border-color: #3498db;
            }}
            .check-title {{
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            .check-score {{
                font-size: 14px;
                color: #7f8c8d;
                margin-bottom: 10px;
            }}
            .score-bar {{
                width: 100%;
                height: 30px;
                background: #ecf0f1;
                border-radius: 4px;
                overflow: hidden;
                margin-bottom: 10px;
            }}
            .score-fill {{
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                font-size: 12px;
            }}
            .status-badge {{
                display: inline-block;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
                color: white;
                margin-bottom: 10px;
                text-transform: uppercase;
            }}
            .details {{
                font-size: 13px;
                color: #555;
                line-height: 1.5;
                font-style: italic;
            }}
            .summary {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin-top: 30px;
                border-left: 4px solid #3498db;
            }}
            .summary-title {{
                font-weight: bold;
                margin-bottom: 10px;
                font-size: 16px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}
            th, td {{
                padding: 10px;
                text-align: left;
                border-bottom: 1px solid #ecf0f1;
            }}
            th {{
                background: #f8f9fa;
                font-weight: bold;
            }}
            .footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #7f8c8d;
                border-top: 1px solid #ecf0f1;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Research Readiness Scorer Report</h1>
                <div class="score-display">{total_score:.1f}</div>
                <div class="score-max">out of 100</div>
            </div>
            
            <div class="content">
                <div class="summary">
                    <div class="summary-title">Summary</div>
                    <table>
                        <thead>
                            <tr>
                                <th>Category</th>
                                <th>Score</th>
                                <th>Status</th>
                                <th>Details</th>
                            </tr>
                        </thead>
                        <tbody>
    """
    
    # Generate table rows
    for key, value in results.items():
        status_color = status_colors.get(value['status'], '#95a5a6')
        html += f"""
                            <tr>
                                <td><strong>{key.replace('_', ' ').title()}</strong></td>
                                <td>{value['score']:.0f}/100</td>
                                <td><span class="status-badge" style="background-color: {status_color};">{value['status']}</span></td>
                                <td>{value['details']}</td>
                            </tr>
        """
    
    html += """
                        </tbody>
                    </table>
                </div>
                
                <h2 style="margin-top: 40px; margin-bottom: 20px; color: #333;">Detailed Breakdown</h2>
                <div class="checks-grid">
    """
    
    # Generate check cards
    for key, value in results.items():
        status_color = status_colors.get(value['status'], '#95a5a6')
        score_percentage = value['score']
        
        html += f"""
                    <div class="check-card">
                        <div class="check-title">{key.replace('_', ' ').title()}</div>
                        <span class="status-badge" style="background-color: {status_color};">{value['status']}</span>
                        <div class="check-score">Score: <strong>{value['score']:.0f}/100</strong></div>
                        <div class="score-bar">
                            <div class="score-fill" style="width: {score_percentage}%; background-color: {status_color};">
                                {score_percentage:.0f}%
                            </div>
                        </div>
                        <div class="details">{value['details']}</div>
                    </div>
        """
    
    html += """
                </div>
            </div>
            
            <div class="footer">
                <p>Generated by Research Readiness Scorer</p>
                <p>This report evaluates repository readiness for research use based on documentation, testing, CI/CD, versioning, and more.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open("report.html", "w") as f:
        f.write(html)
import os
import re
from utils.file_utils import find_file, search_keyword_in_file

def check_citation(repo_path):
    """
    Enhanced citation check scoring 0-100 points:
    - CITATION.cff or equivalent: 35 points
    - DOI or paper reference: 35 points
    - Citation info in README: 20 points
    - Zenodo/artifact identifier: 10 points
    """
    score = 0
    details_list = []
    
    # Check for CITATION files in multiple formats
    citation_files = find_file(repo_path, [
        "CITATION.cff", "CITATION.bib", "CITATION.txt", 
        "CITE.md", "cite.md", "CITE.bib", "codemeta.json"
    ])
    
    if citation_files:
        score += 35
        file_format = os.path.basename(citation_files).split('.')[-1]
        details_list.append(f"Citation file found ({file_format} format)")
    
    # Check README for citation info
    readme = find_file(repo_path, ["README.md", "README.txt", "README.rst"])
    if readme:
        try:
            with open(readme, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                content_lower = content.lower()
                
                # Check for DOI
                doi_pattern = r'10\.\d+/[\w./-]+'
                if re.search(doi_pattern, content) or "doi:" in content_lower:
                    score += 35
                    details_list.append("DOI found")
                
                # Check for paper/publication references
                if any(keyword in content_lower for keyword in ["paper", "publication", "cite", "citation", "arxiv", "zenodo"]):
                    if not any("doi" in d.lower() for d in details_list):  # Don't double count
                        score += min(20, 35 - score)  # Up to 35 for DOI/paper
                    
                    if "zenodo" in content_lower or "arxiv" in content_lower:
                        score += min(10, 100 - score)  # Zenodo/ArXiv ID
                        details_list.append("Research artifact identifier found")
                    else:
                        details_list.append("Publication reference found")
        except:
            pass
    
    # Mention in README counts if no citation files
    if score == 0 and readme:
        try:
            with open(readme, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read().lower()
                if "cite" in content or "citation" in content:
                    score += 20
                    details_list.append("Citation info mentioned in README")
        except:
            pass
    
    status = "excellent" if score >= 90 else "good" if score >= 70 else "fair" if score >= 50 else "poor"
    
    if score == 0:
        status = "missing"
        details = "No citation information found"
    else:
        details = "; ".join(details_list)
    
    return {
        "score": min(score, 100),
        "status": status,
        "details": details
    }
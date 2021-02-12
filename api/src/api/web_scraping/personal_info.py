import requests

from bs4 import BeautifulSoup

DEFAULT_CITATION_RESULTS = {
    "citations": "570",
    "h-index": "14",
    "i-index": "17"
}

def _get_citation_metrics():
    page = requests.get("https://scholar.google.com/citations?user=DxFljRYAAAAJ&hl=en")
    soup = BeautifulSoup(page.content, 'html.parser')
    results=soup.find(id="gsc_rsb_st")
    results_list = results.find_all('td', class_="gsc_rsb_std")
    return {
        "citations": results_list[0].text,
        "h-index": results_list[2].text,
        "i-index": results_list[4].text
    }

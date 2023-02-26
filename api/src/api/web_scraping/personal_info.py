import requests

from bs4 import BeautifulSoup

DEFAULT_CITATION_RESULTS = {
    "citations": "570",
    "h-index": "14",
    "i-index": "17"
}

def get_citation_metrics():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page = requests.get("https://scholar.google.com/citations?user=DxFljRYAAAAJ&hl=en", headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    results=soup.find(id="gsc_rsb_st")
    results_list = results.find_all('td', class_="gsc_rsb_std")
    return {
        "citations": results_list[0].text,
        "h-index": results_list[2].text,
        "i-index": results_list[4].text
    }

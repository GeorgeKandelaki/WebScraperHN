import requests
from bs4 import BeautifulSoup
import pprint


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k["votes"], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        # title = links[idx].getText()
        # href = links[idx].get("href", None)
        title = item.getText()
        href = item.get("href", None)
        vote = subtext[idx].select(".score")
        if len(vote):
            points = int(vote[0].getText().replace(" points", ""))
            if points > 99:
                hn.append({"title": title, "link": href, "votes": points})
    return sort_stories_by_votes(hn)


URL = "https://news.ycombinator.com/?p=1"

results = []
pages_to_scrape = 4
results_length = 0

for page in range(1, pages_to_scrape):
    res = requests.get(URL.replace("p=1", f"p={page}"))
    soup = BeautifulSoup(res.text, "html.parser")
    links = soup.select(".titleline > a")
    subtext = soup.select(".subtext")
    for hn in create_custom_hn(links, subtext):
        results.append(hn)
    results_length = len(results)

pprint.pprint(results_length)
pprint.pprint(results)

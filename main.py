import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def main():
    args = sys.argv[1:]
    url = args[0]
    o = urlparse(url)
    query = parse_qs(o.query)
    url = o._replace(query=None).geturl()
    r = requests.get(url, params=query)
    soup = BeautifulSoup(r.text)

    print(soup.article.header.time.string)
    print(soup.select_one(".byline-prefix").next_sibling.string)
    print(soup.article.header.h1.string)
    for articleBody in (soup.select(".StoryBodyCompanionColumn")):
        if articleBody.em:
            articleBody.em.clear()
        print(articleBody.get_text())


if __name__ == "__main__":
    main()
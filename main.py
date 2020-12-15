import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

newsWebsitesTraces = {
    "nytimes.com": {
        "date": "article header time",
        "byline": ".byline-prefix + a ",
        "title": "article header h1",
        "content": [".StoryBodyCompanionColumn"]
    },
        "washingtonpost.com": {
        "date": "article .display-date",
        "byline": "article span.author-name",
        "title": "header h1",
        "content": [".article-body"]
    }
}

def main():
    args = sys.argv[1:]
    url, domain, query = getUrlAttributes(args[0])
    r = requests.get(url, params=query)
    soup = BeautifulSoup(r.text)

    print(soup.select_one(newsWebsitesTraces[domain]["date"]).string)
    print(soup.select_one(newsWebsitesTraces[domain]["byline"]).string)
    print(soup.select_one(newsWebsitesTraces[domain]["title"]).string)
    for contentSelector in newsWebsitesTraces[domain]["content"]:
        for articleBody in soup.select(contentSelector):
            if articleBody.em:
                articleBody.em.clear()
            print(articleBody.get_text())

def getDomain(url: str):
    sUrl = url.split('.')
    return '.'.join(sUrl[1:])

def getUrlAttributes(url: str):
    o = urlparse(url)
    return o._replace(query=None).geturl(), getDomain(o.netloc), parse_qs(o.query)


if __name__ == "__main__":
    main()
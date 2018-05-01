import urllib.request
import shutil
from html.parser import HTMLParser

parsed_links = set()


def crawl_pages(page):
    global parsed_links

    local_links = set()
    page_links = {page: local_links}

    for link in page_links:
        local_links.add(link)
        if link not in parsed_links:
            crawl_pages(link)


def save_page(page):
    with urllib.request.urlopen(url) as response, open(f"sample.html",
                                                       'wb') as out_file:
        shutil.copyfileobj(response, out_file)


class LinkExtractor(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        attr = dict(attrs)
        global parsed_links
        parsed_links.add(attr.get('href', 'link not available'))


if __name__ == "__main__":
    url = "http://eclipse-phase.wikia.com/wiki/Local_Sitemap"
    base_url = "http://eclipse-phase.wikia.com"
    save_page(url)
    parser = LinkExtractor()
    with open("sample.html", "rb") as f:
        for line in f:
            parser.feed(str(line))
    with open("parsed_links.txt", "w+") as f:
        for i in parsed_links:
            f.write(f"{i}\n")

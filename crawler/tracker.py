import urllib.request
import urllib
import shutil
from html.parser import HTMLParser

parsed_links = set()
visited_links = set()

def crawl_pages(page, parser):
    global parsed_links
    global visited_links

    base_url = "https://eclipse-phase.wikispaces.com/"

    if 'http' not in page:
        page = base_url + page

    local_links = set()
    page_links = {page: local_links}

    for link in page_links:
        local_links.add(link)
        if link not in visited_links:
            crawl_pages(link, parser)

    try:
        name = urllib.quote_plus(page)
        save_page(url, name)

        with open(f"html/{name}.html", "rb") as f:
            for line in f:
                parser.feed(str(line))

    except Exception as e:
        """
        Complete URL is not available from the page so trying to build it
        manually, but need to catch and analyze errors.
        """
        with open(f"handle.txt", "a+") as f:
            f.write(str(e))

def save_page(page, filename):
    with urllib.request.urlopen(page) as response, open(f"{filename}.html", 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

class LinkExtractor(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        attr = dict(attrs)
        global parsed_links
        parsed_links.add(attr.get('href', 'link not available'))

if __name__ == "__main__":
    url = "https://eclipse-phase.wikispaces.com/"
    parser = LinkExtractor()
    crawl_pages(url, parser)

    with open("parsed_links.txt", "w+") as f:
        for i in parsed_links:
            f.write(f"{i}\n")

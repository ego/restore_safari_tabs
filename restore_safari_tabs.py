"""
restore_safari_tabs.py

This script parse safari tabs from files:

    ~/Library/Safari/History.db
    ~/Library/Safari/RecentlyClosedTabs.plist
    ~/Library/Safari/LastSession.plist
    ~/Library/Safari/TopSites.plist

and create index.html in current folder.

Copy files into current folder for accesses.
"""

import logging
from pathlib import Path
import sqlite3
import plistlib


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")


with open("URL_NOT_LIKE.txt") as fd:
    URL_NOT_LIKE = [f"AND url NOT LIKE '{i.strip()}'" for i in tuple(fd.readlines())]


with open("DOMAIN_EXPANSION_NOT_IN.txt") as fd:
    DOMAIN_EXPANSION_NOT_IN = tuple(i.strip() for i in fd.readlines())


def recently_closed_tabs():
    logger.info("Start process RecentlyClosedTabs.plist")
    with open("RecentlyClosedTabs.plist", "rb") as fp:
        data = plistlib.load(fp)

    urls = []
    for item in data["ClosedTabOrWindowPersistentStates"]:
        val = item["PersistentState"].get("TabURL")
        if val:
            urls.append(val)
    logger.info("Finish process RecentlyClosedTabs.plist count %s", len(urls))
    return urls


def last_session():
    logger.info("Start process LastSession.plist")
    with open("LastSession.plist", "rb") as fp:
        data = plistlib.load(fp)

    urls = []
    for item in data["SessionWindows"]:
        for tab in item.get("TabStates"):
            val = tab.get("TabURL")
            if val:
                urls.append(val)

    logger.info("Finish process LastSession.plist count %s", len(urls))
    return urls


def top_sites():
    logger.info("Start process TopSites.plist")
    with open("TopSites.plist", "rb") as fp:
        data = plistlib.load(fp)

    urls = []
    for item in data["TopSites"]:
        val = item.get("TopSiteURLString")
        if val:
            urls.append(val)

    logger.info("Finish process TopSites.plist %s", len(urls))
    return urls


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def history():
    logger.info("Start process History.db")
    conn = sqlite3.connect("History.db")
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    query = f"""
        SELECT DISTINCT history_items.url FROM history_items WHERE
        visit_count > 1
        {' '.join(URL_NOT_LIKE)}
        AND domain_expansion NOT IN {DOMAIN_EXPANSION_NOT_IN}
        ORDER BY id DESC, visit_count DESC, visit_count_score DESC;
    """
    # logger.info("Query:\n %s", query)
    rows = cursor.execute(query)
    urls = [row["url"] for row in rows]
    logger.info("Finish process History.db count %s", len(urls))
    return urls


def build_html(urls):
    logger.info("Start build URLS HTML")
    html = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>URLS</title>
      </head>
      <body>
        <h1>URLS</h1>
        <ul style="list-style-type:none;">
        {}
        </ul>
      </body>
    </html>
    """
    li = [
        f"<li><span>{index}</span> - <a href='{url}'>{url}</a></li>"
        for index, url in enumerate(urls)
    ]
    with open("index.html", "w") as fd:
        fd.write(html.format("".join(li)))
    logger.info("Finish build URLS HTML")


def main():
    history_data = history()
    tabs_data = recently_closed_tabs()
    sites_data = top_sites()
    session_data = last_session()

    urls = set(history_data + tabs_data + sites_data) - set(session_data)
    count = len(urls)
    logger.info("Result count %s", count)

    build_html(urls)


if __name__ == "__main__":
    main()

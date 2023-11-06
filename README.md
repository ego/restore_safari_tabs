# Moved to https://github.com/ego/MacOps/blob/main/restore_safari_tabs/README.md

## restore_safari_tabs.py

This script parse safari tabs from files:

    ~/Library/Safari/History.db
    ~/Library/Safari/RecentlyClosedTabs.plist
    ~/Library/Safari/LastSession.plist
    ~/Library/Safari/TopSites.plist

and create index.html in current folder with all URLS.


## Requirements
* python3


## Pre-requirements
Before run script you need to copy files: 

    ~/Library/Safari/History.db
    ~/Library/Safari/RecentlyClosedTabs.plist
    ~/Library/Safari/LastSession.plist
    ~/Library/Safari/TopSites.plist

into current folder due to problem with accesses to files from bash in macos.


## Configure
Put your SQL `LIKE` strings in file: `URL_NOT_LIKE.txt` for skip this URL.
Put your strings in file: `DOMAIN_EXPANSION_NOT_IN.txt` for skip this domain.


Run script:
`python3 restore_safari_tabs.py`

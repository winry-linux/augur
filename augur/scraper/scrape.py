#!/usr/bin/env python

#   This file is part of Augur - <http://github.com/winry-linux/augur>
#
#   Copyright 2017, Joshua Strot <joshua@winrylinux.org>
#
#   Augur is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Augur is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Augur. If not, see <http://www.gnu.org/licenses/>.

import urllib.request

from sys import stdout
from bs4 import BeautifulSoup
from yaml import dump, CDumper as Dumper


def scrapeAur(aurUrl, cacheFile, perPage=250):
    """
    Scrape a list of packages and versions from the AUR. Iterates over each page,
    downloads it, and then parses it into a list of compiled package names and
    versions. There is no current API to fetch a list of both package names and
    versions, so currently this is the only way to do this. To speed it up, the
    ammount per page is set at the highest value, 250, but if for some reason
    you would want to use less you could lower it. Does use CDumper vs. PyYAML
    default Dumper.

    Currently this process takes quite a while to complete, and some optimization
    could perhaps be done, but it's intentional that this isn't multi-threaded.
    As it stands this already puts quite a burden on AUR servers, and any effort
    to increase the ammount of requests over a period of time would only
    exasperate this.

    Parameters
    ----------
    aurUrl : str
        The URL of the AUR with a valid web protocol specified, such as
        ``https://`` or ``http://``. Do not a leading forward slash.
    cacheFile : str
        The path to the user's local cache file. Should be a full path.
    perPage : int
        The ammount of packages per page to request for scraping. Should for most
        purposes be left alone, but can be changed to 50, 100, 250.

    Returns
    -------
    bool
        This will return True if finished scraping and was able to dump to a
        cache file, but otherwise False.

    """
    print("=> Now scraping the packages from the AUR")

    # Define some variables to assist in the URL
    start = 0
    webpath = "%(aurUrl)s/packages/?O=%(start)s&C=0&SeB=nd&SB=n&SO=a&PP=%(perPage)s&do_Search=Go"

    # Download the total ammount of pages
    initialDownload = urllib.request.urlopen(webpath % locals()).read()
    soup = BeautifulSoup(initialDownload, "html.parser")
    packagesQuant = soup.find("div", {"class": "pkglist-stats"})

    pagesTotal = int(packagesQuant.p.get_text().split(" ")[-1].replace("\t", "").replace(".", ""))

    # Begin iterating to build the list of packages
    packages = {}
    for page in range(1, pagesTotal):
        stdout.write("\r    => Scraping page %(page)s of %(pagesTotal)s" % locals())

        packagesRaw = urllib.request.urlopen(webpath % locals()).read()
        soup = BeautifulSoup(packagesRaw, "html.parser")
        for tr in soup.find("table", {"class": "results"}).tbody.findAll("tr"):
            packages[tr.findAll("td")[0].get_text()] = tr.findAll("td")[1].get_text()

        start = page * perPage
        stdout.flush()

    stdout.write("\r    => Finished scraping.           \n")

    # Write contents to cache
    print("=> Dumping scrape to cache.")
    try:
        with open(cacheFile, "w") as cache:
            dump(packages, cache, encoding="utf-8", default_flow_style=False, Dumper=Dumper)
    except IOError as e:
        print("=> Error! Could not write to cache.")
        return False

    # Finished
    print("=> Update complete.")
    return True

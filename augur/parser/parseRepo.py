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

from urllib import request
from tarfile import open as tarOpen

def downloadDatabase(mirror):
    """Download the database from a specific mirror"""

    print("=> Downloading database from mirror")

    request.urlretrieve("%(mirror)s/winry-testing/winry-testing.db" % locals(), "/tmp/winry-testing.db")

def parsePackages(mirror):
    """Parse a tarred pacman database and find the packages and versions. This is basically a wrapper"""

    #Download an updated database into the /tmp directory
    downloadDatabase(mirror)

    #Open the database as an archive
    archive = tarOpen("/tmp/winry-testing.db")
    packagesRaw = [package for package in archive.getnames() if "/" not in package]

    #Parse database into dictionary
    packages = {}
    for package in packagesRaw:
        packages[package.rsplit("-", 2)[0]] = "-".join(package.rsplit("-", 2)[1:])

    return packages

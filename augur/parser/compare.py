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

import subprocess

def vercmpCompare(winry, aur):
    """Compare two versions with vercmp and return the result"""

    vercmpRaw = subprocess.run(["vercmp", winry, aur], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return vercmpRaw.stdout.decode("utf-8").strip()

def compare(winry, aur, blacklist):
    """Compare package versions between winry linux repos and AUR upsteam"""

    print("=> Parsing packages to compare")

    #Grab list of shared packs
    aurPacks = list(aur.keys())
    winryPacks = list(winry.keys())

    sharedPacks = set(aurPacks).intersection(winryPacks)

    #Begin comparing
    results = False
    for pack in sharedPacks:
        if pack not in blacklist["blacklist"]:
            vercmpCode = vercmpCompare(winry[pack], aur[pack])

            if vercmpCode == "-1":
                print("    => Upgrade: %(pack)s" % locals())
                print("".join(["        => winry: ", winry[pack]]))
                print("".join(["        => AUR:   ", aur[pack]]))
                results = True
            elif vercmpCode == "1":
                print("    => Downgrade: %(pack)s" % locals())
                print("".join(["        => winry: ", winry[pack]]))
                print("".join(["        => AUR:   ", aur[pack]]))
                results = True

    if not results:
        print("=> There are no updates or downgrades available.")

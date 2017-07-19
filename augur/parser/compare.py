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
    """
    Compare two versions with ``vercmp`` and return the result. Function does
    directly call ``vercmp`` with subprocess.

    Parameters
    ----------
    winry : str
        Version of the first package in ``vercmp``'s arguments. Better if it's
        also Winry's package version as well.
    aur : str
        Version of the second package in the arguments. Should be the AUR
        version.::

            -1 : if ver1 < ver2
             0 : if ver1 == ver2
             1 : if ver1 > ver2

    Returns
    -------
    str
        Returns the string output of ``vercmp``. The output will either be 0, 1,
        or -1. The meaning of the numbers are as follows:

    """
    vercmpRaw = subprocess.run(["vercmp", winry, aur], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return vercmpRaw.stdout.decode("utf-8").strip()


def compare(winry, aur, blacklist):
    """
    Compare package versions between winry linux repos and AUR upsteam.
    First the program will get the intersection of the Winry packages and the
    AUR packages. This saves time greatly when iterating over them to compare
    versions. Next the function iterates over the list of shared packages and
    checks for version changes, of which the program will display to the screen.
    The algorithm for comparison in this function should ideally be optimized
    in the future to run faster. As is stands, it uses a brute force algorithm
    which is substancially slowly than an applied sorting algorithm.

    Parameters
    ----------
    winry : dict
        All the winry packages as loaded by ``parseRepo.parsePackages()``. All
        the keys should be the names of the packages, and equal to a str version.
    aur : dict
        Dictionary of all the AUR packages from the Cache loaded by
        ``load.loadAurCache()``.
    blacklist : dict
        Dictionary of user defined packages to not be included in this search.
        Loaded from ``blacklist.readBlacklist()``

    Returns
    -------
    bool
        True if there were any upgrades or downgrades to be displayed. False if
        there were not any.


    """
    print("=> Parsing packages to compare")

    # Grab list of shared packs
    aurPacks = list(aur.keys())
    winryPacks = list(winry.keys())

    sharedPacks = set(aurPacks).intersection(winryPacks)

    # Begin comparing
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

    return results

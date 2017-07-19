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

from os import path
from yaml import load, CLoader as Loader

from augur.configuration import configure


def loadAurCache():
    """
    Read and load the cache of AUR packages. Uses CLoader as opposed to PyYAML's
    default Loader. Function will exit if it cannot read the cache.

    Returns
    -------
    dict
        YAML loaded dictionary of packages from the cache.

    """
    print("=> Loading AUR packages from cache")

    # Load xdg cache path
    cachePath = configure.loadXDGVars()["xdgCache"]

    # Load the packages
    packages = {}
    if path.isfile("%(cachePath)s/augur/packages.yaml" % locals()):
        try:
            with open("%(cachePath)s/augur/packages.yaml" % locals(), "r") as file:
                packages = load(file, Loader=Loader)
                if not packages:
                    print("=> Error! Cache is empty. Please update it (-u).")
        except IOError as e:
            print("=> Error! Cache not found. Please update it (-u).")
            exit(1)

    return packages

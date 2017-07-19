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
from yaml import load, dump, CDumper as Dumper, CLoader as Loader

from augur.configuration import configure


def readBlacklist():
    """
    Read the blacklist file and return a dictionary of the packages. The
    dictionary only contains one key, ``"blacklist"``. This function uses
    CLoader as opposed to PyYAML's default Loader.

    Returns
    -------
    dict
        A dictionary containing the list of packages that are blacklisted. The
        dictionary only contains one key, ``"blacklist"`` which contains the
        actual dictionary. This is done on purpose so it will easier in the
        future to expand upon the code and add other types of blacklists.

    """
    # Load xdg config path
    configPath = configure.loadXDGVars()["xdgConfig"]

    # Attempt to read a local blacklist
    blacklistPacks = {}
    blacklist = "%(configPath)s/augur/blacklist.yaml" % locals()
    if path.isfile(blacklist):
        try:
            with open(blacklist, "r") as file:
                blacklistPacks = load(file, Loader=Loader)
                if not blacklistPacks:
                    print("=> Error! Local blacklist found, but empty. Attempting to use global instead.")
        except IOError as e:
            print("=> Error! Local blacklist found but not readable. Falling back to global.")

    # Attempt to load a global if no local one is found.
    if path.isfile("/etc/augur/blacklist.yaml") and not blacklistPacks:
        try:
            with open("/etc/augur/blacklist.yaml", "r") as file:
                blacklistPacks = load(file, Loader=Loader)
                if not blacklistPacks:
                    print("=> Error! Global blacklist found but empty.")
        except IOError as e:
            print("=> Error! Global blacklist found but not readable.")
    elif not path.isfile("/etc/augur/blacklist.yaml") and not blacklistPacks:
        print("=> Error! No global or local blacklist found.")
        blacklistPacks["blacklist"] = []

    return blacklistPacks


def addBlacklist(package):
    """
    Add a package to the list of blacklisted packages. This will open and load
    the local blacklist file with yaml, append the package to list, and then
    dump it back. It's worth noting that CDumper is used rather than the default
    PyYAML dumper. This function will exit the program if it could not write to
    the blacklist, or if the package was already blacklisted.

    Parameters
    ----------
    package : str
        Name of the package to be blacklisted. Must be the exact package name as
        defined in the package's PKGBUILD ``pkgname`` variable.

    """
    configPath = configure.loadXDGVars()["xdgConfig"]

    # Load the current blacklist information
    blacklistPacks = readBlacklist()

    # Do some quick error proofing
    if package in blacklistPacks["blacklist"]:
        print("=> Error! Package already blacklisted.")
        exit(1)

    # Write the new information if it is safe
    try:
        with open("%(configPath)s/augur/blacklist.yaml" % locals(), "w+") as file:
            blacklistPacks["blacklist"].append(package)
            dump(blacklistPacks, file, encoding="utf-8", Dumper=Dumper)
    except IOError as e:
        print("=> Error! Could not write to blacklist.")
        exit(1)

    print("=> Added %(package)s to blacklist" % locals())


def printBlacklist():
    """
    Load the blacklist, and then print the results to screen. Uses the
    ``readBlacklist()`` function.

    Returns
    -------
    bool
        True if the blacklist contained packages to be printed to the screen,
        otherwise False is the blacklist did not contain any blacklist packages.
    """
    configPath = configure.loadXDGVars()["xdgConfig"]

    # Load the current blacklist information
    blacklistPacks = readBlacklist()

    if not blacklistPacks["blacklist"]:
        print("=> Nothing blacklisted.")
        return False

    print("=> Blacklisted:")
    for pack in blacklistPacks["blacklist"]:
        print("    => %(pack)s" % locals())
    return True


def whitelist(package):
    """
    Remove a package from the blacklist, or "whitelist" the package. This will
    read the blacklist using the ``readBlacklist()`` function, and then attempt
    to remove the specified package from the blacklist. The program will be
    exited if the package is not in the blacklist, or if the blacklist is
    unreadable.

    Parameters
    ----------
    package : str
        The package to be whitelisted. Must be the exact package name as
        defined in the package's PKGBUILD ``pkgname`` variable.

    """
    configPath = configure.loadXDGVars()["xdgConfig"]

    # Load the current blacklist information
    blacklistPacks = readBlacklist()

    # Do some quick error proofing
    if package not in blacklistPacks["blacklist"]:
        print("=> Error! Package not blacklisted")
        exit(1)

    # Write the new information if it is safe
    try:
        with open("%(configPath)s/augur/blacklist.yaml" % locals(), "w+") as file:
            blacklistPacks["blacklist"].remove(package)
            dump(blacklistPacks, file, encoding="utf-8", Dumper=Dumper)
    except IOError as e:
        print("=> Error! Could not write to blacklist.")
        exit(1)

    print("=> Whitelisted %(package)s" % locals())

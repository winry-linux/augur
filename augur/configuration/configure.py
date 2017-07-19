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

from os import environ, path, makedirs
from yaml import load


def loadXDGVars():
    """
    Attempt to load the ``XDG_CONFIG_HOME`` and ``XDG_CACHE_HOME`` environmental
    variables. If not set, then defaults to ``~/.config`` and ``~/.cache``
    respectively.

    Returns
    -------
    dict
        A dictionary containing the environmental variables, with
        ``"xdgConfig"`` and ``"xdgCache"`` as keys representing the values
        determined.

    """
    # Grab the XDG Config Path
    if environ.get("XDG_CONFIG_HOME"):
        xdgConfig = environ["XDG_CONFIG_HOME"]
    else:
        xdgConfig = path.expanduser("~") + "/.config"

    # Grab the XDG Cache Path
    if environ.get("XDG_CACHE_HOME"):
        xdgCache = environ["XDG_CACHE_HOME"]
    else:
        xdgCache = path.expanduser("~") + "/.cache"

    return {"xdgConfig": xdgConfig, "xdgCache": xdgCache}


def checkConfiguration(configuration):
    """
    Check that the configuration file is both sane. Namely, the function looks
    for ``"AURUrl"`` and ``"Mirror"`` values to be defined.

    Parameters
    ----------
    configuration : dict
        A YAML loaded dictionary of the configuration file to be checked.

    Returns
    -------
    bool
        True if the configuration file has both required values set, otherwise
        False if they are not defined or set.

    """
    if "AURUrl" not in configuration.keys() or "Mirror" not in configuration.keys():
        print("Error! Not configured correctly.")
        return False
    return True


def loadConfiguration():
    """
    Attempt to load the configuration settings from one of the configuration
    files. First, attempt to load them from a local user defined file, but if
    not available then the settings will be loaded from the global file. This
    function will exit if unable load both a local and global configuration file.

    Returns
    -------
    dict
        A YAML configuration file loaded from either local or global paths.

    """
    # Load some XDG Vars
    xdgVars = loadXDGVars()
    xdgConfig = xdgVars["xdgConfig"]

    # Attempt to load a local configuration first
    configFile = None
    if path.isfile("%(xdgConfig)s/augur/configuration.yaml" % locals()):
        try:
            with open("%(xdgConfig)s/augur/configuration.yaml" % locals(), "r") as file:
                configFile = load(file)
        except IOError as e:
            print("=> Error! Local configuration found but not readable, falling back to default")

    # Looks like a local one wasn't found, so see if a system one is set and configured
    if not configFile:
        if path.isfile("/etc/augur/configuration.yaml"):
            try:
                with open("/etc/augur/configuration.yaml") as file:
                    configFile = load(file)
            except IOError as e:
                print("=> Error! Global configuration found but not readable. Exiting.")
                exit(1)
        else:
            print("=> Error! No global configuration. Exiting.")
            exit(1)

    # Make sure that the configuration file is sane
    checkConfiguration(configFile)

    return configFile


def checkCache(updating):
    """
    Initialize the cache files for the user. Just create the needed path if not
    already present, verify the user would like to overwrite the current cache
    if one exists. This puts the Cache files at ``~/$XDG_CACHE_HOME/augur``. The
    function will exit if the user does not verify to overwriting current cache.
    Optionally, the verification can be bypassed with the ``updating`` parameter.

    Parameters
    ----------
    updating : bool
        True will make the function check for presence an already existing cache
        and prompt the user if they are sure they would like to overwrite it.
        False will skip that process entirely, and just create the path to the
        cache. True should be used if the cache is going to be overwritten,
        whereas False should be used if the cache is merely being read.

    Returns
    -------
    str
        The full path to the user's local cache file.

    """
    # Load some XDG Vars
    xdgVars = loadXDGVars()
    xdgCache = xdgVars["xdgCache"]

    # Make a cache if not already present
    if not path.isdir("%(xdgCache)s/augur" % locals()):
        print("=> No cache found, creating cache directory.")
        makedirs("%(xdgCache)s/augur" % locals())

    # Make sure user is alright with writing over current cache
    if path.isfile("%(xdgCache)s/augur/packages.yaml" % locals()) and updating:
        print("=> There's already a cache present, are you sure you would like to download another one?")
        verify = input("=[y/N]> ")

        if verify != "y" and verify != "Y":
            print("=> Exiting...")
            exit(1)

    return "%(xdgCache)s/augur/packages.yaml" % locals()

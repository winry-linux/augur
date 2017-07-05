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
    """Load XDG vars"""

    #Grab the XDG Config Path
    if environ.get("XDG_CONFIG_HOME"):
        xdgConfig = environ["XDG_CONFIG_HOME"]
    else:
        xdgConfig = path.expanduser("~") + "/.config"

    #Grab the XDG Cache Path
    if environ.get("XDG_CACHE_HOME"):
        xdgCache = environ["XDG_CACHE_HOME"]
    else:
        xdgCache = path.expanduser("~") + "/.cache"

    return {"xdgConfig": xdgConfig, "xdgCache": xdgCache}

def checkConfiguration(configuration):
    """Check the configuration file to ensure that it's not empty"""
    if "AURUrl" not in configuration.keys() or "Mirror" not in configuration.keys():
        print("Error! Not configured correctly.")
        return False
    return True

def loadConfiguration():
    """Attempt to load configuration settings"""

    #Load some XDG Vars
    xdgVars = loadXDGVars()
    xdgConfig = xdgVars["xdgConfig"]

    #Attempt to load a local configuration first
    configFile = None
    if path.isfile("%(xdgConfig)s/augur/configuration.yaml" % locals()):
        try:
            with open("%(xdgConfig)s/augur/configuration.yaml" % locals(), "r") as file:
                configFile = load(file)
        except IOError as e:
            print("=> Error! Local configuration found but not readable, falling back to default")

    #Looks like a local one wasn't found, so see if a system one is set and configured
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

    #Make sure that the configuration file is sane
    checkConfiguration(configFile)

    return configFile

def checkCache(updating):
    """Initialize the cache files for the user"""

    #Load some XDG Vars
    xdgVars = loadXDGVars()
    xdgCache = xdgVars["xdgCache"]

    #Make a cache if not already present
    if not path.isdir("%(xdgCache)s/augur" % locals()):
        print("=> No cache found, creating cache directory.")
        makedirs("%(xdgCache)s/augur" % locals())

    #Make sure user is alright with writing over current cache
    if path.isfile("%(xdgCache)s/augur/packages.yaml" % locals()) and updating:
        print("=> There's already a cache present, are you sure you would like to download another one?")
        verify = input("=[y/N]> ")

        if verify != "y" and verify != "Y":
            print("=> Exiting...")
            exit(1)

    return "%(xdgCache)s/augur/packages.yaml" % locals()

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

import argparse

from os import geteuid
from sys import argv

from display import *

#Exit if root
if geteuid() == 0:
    print("=> This program cannot be ran as root")
    exit(0)

#Set up the argument parser, add the needed options
parser = argparse.ArgumentParser(description='Check the Winry repository for updates from the AUR.')
parserGroup = parser.add_mutually_exclusive_group()
parserGroup.add_argument('-i', "--init", type=str, metavar="PATH", help="Initialize a list of AUR packages and versions")
parserGroup.add_argument('-u', "--update", action="store_true", help="Update the list of AUR packages and versions")
parserGroup.add_argument('-c', "--check", action="store_true", help="Check the list of AUR packages again the repository")
parserGroup.add_argument('-b', "--blacklist", action="store_true", help="Blacklist a package from being checked")
parserGroup.add_argument('-w', "--whitelist", action="store_true", help="Whitelist a package so it is checked again")
parserGroup.add_argument('-p', "--printblack", action="store_true", help="Print the blacklist")
parserGroup.add_argument('-p', "--printblack", action="store_true", help="Print the blacklist")

#Output help if no argument is passed, exit
if len(argv) == 1:
    asciiArt.banner()
    parser.print_help()
    exit(1)

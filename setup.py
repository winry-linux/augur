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

from setuptools import setup

_packages = [
    'augur',
    'augur.configuration',
    'augur.display',
    'augur.parser',
    'augur.scraper']

_scripts = [
    'augur/augur']

_data_files = [(
    "/etc/augur", ["data/blacklist.yaml", "data/configuration.yaml"])]


setup(
    name="Augur",
    version="0.1.1",
    url="https://github.com/winry-linux/augur",
    license="GPLv3",
    author="Joshua Strot",
    author_email="joshua@winrylinux.org",
    description="Utility to monitor updates for packages pulled from AUR",
    long_description="""Augur is a remake of an older program written for Manjaro, 
    Satori, that has been improved and revamped for Winry. Augur scrapes a list of 
    packages and versions from the AUR, and then compares them with packages that 
    have been pulled into the Winry repository to check for upgrades / downgrades."""
    
    packages=_packages,
    scripts=_scripts,
    data_files=_data_files
)

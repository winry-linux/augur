Hacking on Augur
================
If you would like to contribute to Augur, that's great! Please however keep the following things in mind while doing so to help keep Augur a unified and hacker friendly project. 

Licensing
=========
Augur is released under the terms of the GNU GPL, version 3 or later. Every source file must have a license header, with a list of copyright holders and years.

Example:
```
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
 */
```
Copyright holders must be physical or legal personalities. A statement such as
`Copyright 2014, The FooBarQuux project` has no legal value if "The FooBarQuux
project" is not the legal name of a person, company, incorporated
organization, etc.

Please add your name to files you touch when making any contribution (even if
it's just a typo-fix which might not be copyrightable in all jurisdictions).

Formatting
==========
Augur is formatted according to [Python's PEP-8](https://www.python.org/dev/peps/pep-0008/). Some rules have been bent as they are not as relevent anymore, such as the maximum line length of 79 characters, but try to adhere to the PEP-8 standards as much as possible.

Docstrings
----------
[Numpy style docstrings](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt) are used throughout the program and later pulled into the Sphinx documentation. Use these wherever applicable to document your code so future developer's will have a bit easier time understanding and hacking on it themselves. An example of a Numpy style Docstring would be as follows:

```
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
    perPage : int, optional
        The ammount of packages per page to request for scraping. Should for most
        purposes be left alone, but can be changed to 50, 100, 250.

    Returns
    -------
    bool
        This will return True if finished scraping and was able to dump to a
        cache file, but otherwise False.

    """
```

Naming
------
* Use camelCase for everything.
* Local variables should start out with a lowercase letter.
* Class names are capitalized

Imports
-------
When importing modules avoid star, or wildcard, imports. The exception to the rule is unless it is a module written in the program itself. Even then it should be avoided if reasonable.

Linting
=======
Since Python is not compiled, some bugs or typographical errors can lurk beneath the surface and not be discovered right away. Linting helps discover problems that you may not have seen yourself, so always make sure to lint the source directory before commiting it. 

PyLint
------
The preferred linter for this project is `pylint`, and can be ran as follows:

```
pylint augur
```

Flake8
------
Augur was programmed in Atom with the `flake8` linter plugin, so it is also validated with it. If you would rather use `flake8`, you can do so as follows. 

```
flake8 augur --ignore E501
```

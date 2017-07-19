Augur
=====
Augur is a remake of one of my older programs written for [Manjaro](https://manjaro.org "Manjaro Linux"), [Satori](https://github.com/joshuastrot/satori), that has been improved and revamped for [Winry](https://winrylinux.org "Winry Linux"). Augur scrapes a list of packages and versions from the AUR, and then compares them with packages that have been pulled into the [Winry repository](https://repo.winrylinux.org "Winry Linux Repository") to check for upgrades / downgrades.

Features:
* Scrapes a list of all AUR packages and versions
* Cache's scrapes so that you don't need to constantly rescrape
* Has a configuration file that allows you to change Mirror url
* Provides a black list to ignore packages from being checked
* Command line options to blacklist and whitelist packages

Installation
============
On Winry Linux, Augur can be installed directly with Pacman

```bash
sudo pacman -Sy augur
```

Dependencies
------------
```
python-yaml
python-beautifulsoup4
yaml-cpp
```

Usage
=====
To display a help menu for Augur, simple run `augur`
```bash
augur
```

Configuring
===========
Augur can run perfectly fine without configuring, however there are some configuration options you can configure. You can configure them globally by editing them in `/etc/augur`, but if you would like to make the configurations effective only for your user, copy them to `$HOME/.config/augur`.

Documentation
=============
Augur has very detailed Numpy style docstrings throughout the code for reference, and Sphinx docs already set up. If you would like to build some docs for reference, you can navigate to the docs and run `make builder`, where `builder` is any one of the available builder formats available from sphinx. To see a full list of builder's, see [Sphinx Documentation](http://www.sphinx-doc.org/en/stable/builders.html). Please note that you will need to install the numpydocs python module to do this however.

Authors
=======
* Joshua Strot - joshua@winrylinux.org

License
=======
This project is licensed under the GNU General Public License. See [LICENSE](LICENSE) for more details.

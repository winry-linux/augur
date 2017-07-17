from setuptools import setup

setup(
    name="Augur",
    version="0.1",
    url="https://github.com/winry-linux/augur",
    license="GPLv3",
    author="Joshua Strot",
    author_email="joshua@winrylinux.org",
    description="Utility to monitor updates for packages pulled from AUR",
    
    packages=['augur', 'augur.configuration', 'augur.display', 'augur.parser', 'augur.scraper'],
    scripts=["augur/augur"],
    data_files=[("/etc/augur", ["data/blacklist.yaml", "data/configuration.yaml"])]
)

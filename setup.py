# -*- coding: utf-8 -*-

import os
from setuptools import find_packages


here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, "conrad", "__version__.py"), "r") as f:
    exec(f.read(), about)

with open("README.md", "r") as f:
    readme = f.read()


requires = [
    "Click>=7.0",
    "cli-helpers>=1.2.1",
    "colorama>=0.4.1",
    "geopy>=2.0.0",
    "requests>=2.22.0",
    "SQLAlchemy>=1.3.10",
    "textdistance>=4.1.5",
]
dev_requires = ["Sphinx>=2.2.1", "pytest>=3.8.0"]
crawl_requires = [
    "beautifulsoup4>=4.8.1",
    "Cerberus>=1.3.2",
    "dateparser>=0.7.2",
    "GitPython>=3.1.18",
    "google-api-python-client>=1.10.0",
    "pandas>=0.25.2",
    "pyOpenSSL>=19.0.0",
    "requests>=2.22.0",
    "textdistance>=4.1.5",
]
dev_requires = dev_requires + requires
all_requires = crawl_requires + dev_requires


def setup_package():
    metadata = dict(
        name=about["__title__"],
        version=about["__version__"],
        description=about["__description__"],
        long_description=readme,
        long_description_content_type="text/markdown",
        url=about["__url__"],
        author=about["__author__"],
        author_email=about["__author_email__"],
        license=about["__license__"],
        packages=find_packages(exclude=("tests",)),
        install_requires=requires,
        extras_require={"all": all_requires, "dev": dev_requires},
        entry_points={"console_scripts": ["conrad = conrad.__main__:main"]},
        classifiers=[
            # Trove classifiers
            # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
        ],
    )

    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup

    setup(**metadata)


if __name__ == "__main__":
    setup_package()

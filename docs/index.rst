.. conference-radar documentation master file, created by
   sphinx-quickstart on Tue Oct 29 12:04:29 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

conrad — Conference Radar
=========================

.. image:: https://github.com/vinayak-mehta/conrad/workflows/Get%20events/badge.svg
    :target: https://github.com/vinayak-mehta/conrad/workflows/Get%20events/badge.svg
    :alt: Workflow Status

.. image:: https://readthedocs.org/projects/conference-radar/badge/?version=latest
    :target: https://conference-radar.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/conference-radar.svg
    :target: https://pypi.org/project/conference-radar/

.. image:: https://img.shields.io/pypi/pyversions/conference-radar.svg
    :target: https://pypi.org/project/conference-radar/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

.. image:: https://img.shields.io/badge/continous%20quality-deepsource-lightgrey
    :target: https://deepsource.io/gh/vinayak-mehta/conrad/?ref=repository-badge

``conrad`` helps you track conferences and meetups on your terminal!

---

Here's how it works::

    $ conrad show

.. csv-table::

    id,name,url,city,state,country,start_date,end_date
    3ae4f9,PyCon Fr 2019,https://www.pycon.fr/,Bordeaux,,France,2019-10-31,2019-11-04
    68bf57,PyCon Sweden,http://www.pycon.se/,Stockholm,,Sweden,2019-10-31,2019-11-02

Why conrad?
-----------

- 🤖 The event database updates automatically using crawlers + GitHub Actions.
- 📅 Never miss CFP deadlines again. ``conrad remind`` can remind you every time you open a terminal!
- 📊 Query and explore events using tags, names, locations, and dates. ``conrad show --cfp`` will tell you about events where the cfp is open!
- 🔄 Run ``conrad refresh`` to get the latest events!
- ⛏️ You can contribute crawlers and events by simply raising a PR!

Installation
------------

You can simply use pip to install ``conrad``::

    $ pip install conference-radar

Contributing
------------

The `Contributor's Guide <https://github.com/vinayak-mehta/conrad/blob/master/CONTRIBUTING.md>`_ has detailed information about guidelines around contributions. You can add new crawlers and events to ``conrad``!

.. toctree::
   :maxdepth: 2

   dev/adding-crawlers
   dev/adding-events

Versioning
----------

``conrad`` uses `Semantic Versioning <https://semver.org/>`_. For the available versions, see the tags on the GitHub repository.

License
-------

This project is licensed under the Apache License, see the `LICENSE <https://github.com/vinayak-mehta/conrad/blob/master/LICENSE>`_ file for details.

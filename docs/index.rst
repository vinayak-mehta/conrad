.. conference-radar documentation master file, created by
   sphinx-quickstart on Tue Oct 29 12:04:29 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

conrad — Conference Radar
=========================

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

- 📅 Never miss CFP deadlines again. ``conrad remind`` can remind you every time you open a terminal!
- 📊 Query and explore events using tags, names, locations, and dates. ``conrad show --cfp`` will tell you about events where the cfp is open!
- 🔄 Run ``conrad refresh`` to get the latest events!
- 🤖 (`upcoming <https://github.com/vinayak-mehta/conrad/issues/17>`_) The event database updates automatically with events curated by the community.
- ⛏️ You can manually add events using ``conrad import -f events.json`` and raise a PR!

Installation
------------

You can simply use pip to install ``conrad``::

    $ pip install conference-radar

Versioning
----------

``conrad`` uses `Semantic Versioning <https://semver.org/>`_. For the available versions, see the tags on the GitHub repository.

License
-------

This project is licensed under the Apache License, see the `LICENSE <https://github.com/vinayak-mehta/conrad/blob/master/LICENSE>`_ file for details.

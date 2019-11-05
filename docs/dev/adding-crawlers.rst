.. _adding-crawlers:

Adding a crawler
================

``conrad``'s event database is updated every Monday at ``00:00 UTC`` using a GitHub workflow. The workflow runs all crawlers, updates the event database and raises a PR for a maintainer to review and then merge. Once the PR is merged, these new events become available for consumption using the command-line interface!

Currently, ``conrad`` has crawlers for:

- http://papercall.io
- https://github.com/python-organizers/conferences

There are two steps you need to do for adding a crawler to ``conrad``, writing a crawler and then scheduling the crawler.

.. note:: Please use the pull request workflow that is described in the `Contributor's Guide <https://github.com/vinayak-mehta/conrad/blob/master/CONTRIBUTING.md>`_.

Writing a crawler
-----------------

All crawlers are present in the ``crawlers`` package at the root of the `GitHub repository <https://github.com/vinayak-mehta/conrad>`_.

This is how the ``crawlers`` package is structured::

    $ tree crawlers
    .
    ├── base.py
    ├── __init__.py
    ├── __main__.py
    ├── papercall
    │   ├── __init__.py
    │   └── papercall_crawler.py
    └── pycon
        ├── __init__.py
        └── pycon_crawler.py

Let's say we want to add a new crawler for a website called "Creepy". We'll start by creating a new module called ``creepy`` at the same level as the other crawler modules (``papercall`` and ``pycon``). This new module should contain two files, ``__init__.py`` and ``creepy_crawler.py``.

The new ``crawlers`` directory structure::

    $ tree crawlers
    .
    ├── base.py
    ├── creepy
    │   ├── creepy_crawler.py
    │   └── __init__.py
    ├── __init__.py
    ├── __main__.py
    ├── papercall
    │   ├── __init__.py
    │   └── papercall_crawler.py
    └── pycon
        ├── __init__.py
        └── pycon_crawler.py

Next, we need to add a class called ``CreepyCrawler`` to ``creepy_crawler.py`` which will contain our crawling logic, in its ``get_events`` method::

    class CreepyCrawler(BaseCrawler):
        def get_events(self):
            # Populate a list of events using a crawling logic
            events = []

            # Extend the self.events list with the new list
            self.events.extend(events)

Finally, we need to add an import for our ``CreepyCrawler`` class to the ``crawlers`` package's ``__init__.py``::

    from .creepy.creepy_crawler import CreepyCrawler

Now that we have written our crawler, we just need to schedule it!

Scheduling the crawler
----------------------

To schedule our ``CreepyCrawler``, we need to update the `workflow definition <https://github.com/vinayak-mehta/conrad/blob/master/.github/workflows/main.yml>`_, by adding the following step (before the "Create pull request" step) to the ``get_events`` job::

    - id: source_name
      name: Get Creepy events action step
      uses: ./.github/actions/get-events-action
      with:
        crawler-name: 'CreepyCrawler'

And that's it, our crawler is now scheduled!

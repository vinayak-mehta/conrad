.. _adding-crawlers:

Adding a crawler
================

``conrad``'s event database is updated every Monday and Thursday at ``00:00 UTC`` using a GitHub workflow. The workflow runs all crawlers, updates the event database and raises a PR for a maintainer to review and then merge. Once the PR is merged, these new events become available for consumption using the command-line interface!

Currently, ``conrad`` has crawlers for:

- https://pydata.org/event-schedule
- https://github.com/python-organizers/conferences
- https://wiki.python.org/moin/PythonEventsCalendar

There are two steps you need to do for adding a crawler to ``conrad``, writing a crawler and then scheduling the crawler.

.. note:: Please use the pull request workflow that is described in the `Contributor's Guide <https://github.com/vinayak-mehta/conrad/blob/master/CONTRIBUTING.md>`_.

Writing a crawler
-----------------

All crawlers are present in the ``crawlers`` package at the root of the `GitHub repository <https://github.com/vinayak-mehta/conrad>`_.

You can use the ``generate`` command to generate the base code for your crawler::

    $ conrad generate crawler Creepy
        create	crawlers/creepy/creepy_crawler.py

And then add your crawling code to the generated file which will be used to populate the events list::

    class ConfsTechCrawler(BaseCrawler):
        def get_events(self):
            # Populate this list of events using your code
            events = []

            # YOUR CODE HERE

            # Extend the self.events list with the new list
            self.events.extend(events)

You can use the ``run`` command to see if your data is getting saved in the format specified in :ref:`adding-events`::

    $ conrad run crawler Creepy
        save	data/creepy.json

After you're finished writing your crawling code, you just need to schedule it.

Scheduling the crawler
----------------------

To schedule the newly added ``CreepyCrawler``, you need to update the `workflow definition <https://github.com/vinayak-mehta/conrad/blob/master/.github/workflows/main.yml>`_, by adding the following step (before the "Create pull request" step) to the ``get_events`` job::

    - id: source_name
      name: Get Creepy events action step
      uses: ./.github/actions/get-events-action
      with:
        crawler-name: 'CreepyCrawler'

Finally, you can raise a PR, which after getting merged can start populating the events list every Monday and Thursday.

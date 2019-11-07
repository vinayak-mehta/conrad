.. _adding-events:

Adding new events
=================

You can also add new events to ``conrad`` without writing a crawler for them. To do so, please go through the following steps:

1. Create a `new_events.json` file containing the list of events you want to add, with the following fields::

    [
        {
            "name": "PyCon US",
            "url": "https://us.pycon.org",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "country": "USA",
            "cfp_open": true,
            "cfp_end_date": "2019-12-20",
            "start_date": "2020-04-15",
            "end_date": "2020-04-23",
            "source": "https://www.python.org/events/",
            "tags": "['python']",
            "kind": "conference",
            "by": "human",
        }
    ]
    "new_events.json" 17L, 436C

2. Fork the project repository. Click on the ‘Fork’ button near the top of the page. This creates a copy of the code under your account on the GitHub. Clone your fork of conrad from your GitHub account::

    $ git clone https://www.github.com/[username]/conrad
    $ cd conrad

3. Create a branch to hold your changes::

    $ git checkout -b add-new-event

4. Import the new events::

    $ conrad import -f ../new_events.json

5. Finally push your changes and `raise a PR <https://help.github.com/articles/creating-a-pull-request-from-a-fork/>`_::

    $ git add .
    $ git commit -m "Add new events"
    $ git push -u origin add-new-event</pre>

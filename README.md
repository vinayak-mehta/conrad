<p align="center">
   <img src="https://raw.githubusercontent.com/vinayak-mehta/conrad/master/docs/_static/mozilla-satellite-antenna.png" width="200">
</p>

# conrad — Conference Radar

[![Workflow Status](https://github.com/vinayak-mehta/conrad/workflows/Get%20events/badge.svg)](https://github.com/vinayak-mehta/conrad/actions) [![Documentation Status](https://readthedocs.org/projects/conference-radar/badge/?version=latest)](https://conference-radar.readthedocs.io/en/latest/) [![image](https://img.shields.io/pypi/v/conference-radar.svg)](https://pypi.org/project/conference-radar/) [![image](https://img.shields.io/pypi/pyversions/conference-radar.svg)](https://pypi.org/project/conference-radar/) [![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

`conrad` helps you track conferences and meetups on your terminal.

---

Here's how it works:

<pre>
$ conrad show
</pre>

![show](https://raw.githubusercontent.com/vinayak-mehta/conrad/master/docs/_static/show.png)

## Why conrad?

- 📅 Never miss CFP deadlines again. `conrad remind` can remind you every time you open a terminal!
- 📊 Query and explore events using tags, names, locations, and dates. `conrad show --cfp` will tell you about events where the CFP is open!
- 🤖 Crawlers update events twice a week! (Monday and Thursday at 00:00 UTC)

## Installation

You can simply use pip to install `conrad`:

<pre>
$ pip install conference-radar
</pre>

## Features

### Continuous updates

The event list is maintained in `data/events.json`. This list is continuously updated by the available `crawlers` using GitHub Actions.

Sources:

- https://pydata.org/event-schedule
- https://github.com/ildoc/awesome-italy-events
- https://github.com/python-organizers/conferences
- https://wiki.python.org/moin/PythonEventsCalendar
- http://papercall.io (soon)

### Set reminders

You can set CFP reminders so that you never miss a deadline! The color changes based on event proximity; **> 30 days** ![#008000](https://placehold.it/15/008000/000000?text=+), **>10 and < 30 days** ![#ffff00](https://placehold.it/15/ffff00/000000?text=+) and **< 10 days** ![#ff0000](https://placehold.it/15/ff0000/000000?text=+).

<pre>
$ conrad remind -i 6bb714
$ conrad remind
</pre>

![remind](https://raw.githubusercontent.com/vinayak-mehta/conrad/master/docs/_static/remind.png)

**Protip**: Add `conrad remind` to your shell startup file so that you get a reminder every time you open a new terminal!

### Query and explore

You can query and explore the event database using various filters.

Look at events which have an open call for proposals (CFP):

<pre>
$ conrad show --cfp
</pre>

![show-cfp](https://raw.githubusercontent.com/vinayak-mehta/conrad/master/docs/_static/show-cfp.png)

Look at conferences using a tag:

<pre>
$ conrad show --tag python
</pre>

![show-tag](https://raw.githubusercontent.com/vinayak-mehta/conrad/master/docs/_static/show-tag.png)

Look at conferences using a name:

<pre>
$ conrad show --name pycon
</pre>

![show-name](https://raw.githubusercontent.com/vinayak-mehta/conrad/master/docs/_static/show-name.png)

Look at conferences in a city, state or country:

<pre>
$ conrad show --location usa
</pre>

![show-location](https://raw.githubusercontent.com/vinayak-mehta/conrad/master/docs/_static/show-location.png)

Look at conferences based on when they're happening:

<pre>
$ conrad show --date ">= 2019-10-01" --date "<= 2020-01-01"
</pre>

![show-date](https://raw.githubusercontent.com/vinayak-mehta/conrad/master/docs/_static/show-date.png)

### Refresh event database

You can get the latest events using:

<pre>
$ conrad refresh
</pre>

![refresh](https://raw.githubusercontent.com/vinayak-mehta/conrad/master/docs/_static/refresh.png)

## Contributing

The [Contributor's Guide](https://github.com/vinayak-mehta/conrad/blob/master/CONTRIBUTING.md) has detailed information about guidelines around contributions. You can add new crawlers and events to `conrad`:

- [Adding a crawler](https://conference-radar.readthedocs.io/en/latest/dev/adding-crawlers.html)
- [Adding new events](https://conference-radar.readthedocs.io/en/latest/dev/adding-events.html)

## Versioning

`conrad` uses [Semantic Versioning](https://semver.org/). For the available versions, see the tags on this repository.

## License

This project is licensed under the Apache License, see the [LICENSE](https://github.com/vinayak-mehta/conrad/blob/master/LICENSE) file for details.

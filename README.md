# conrad — Conference Radar 📡

[![image](https://img.shields.io/pypi/v/conference-radar.svg)](https://pypi.org/project/conference-radar/) [![image](https://img.shields.io/pypi/l/conference-radar.svg)](https://pypi.org/project/conference-radar/) [![image](https://img.shields.io/pypi/pyversions/conference-radar.svg)](https://pypi.org/project/conference-radar/) [![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

`conrad` helps you track conferences and meetups on your terminal!

Here's how it works:

<pre>
$ conrad show
</pre>

| id     | name               | url                               | city             | state  | country | start_date | end_date   |
|--------|--------------------|-----------------------------------|------------------|--------|---------|------------|------------|
| c987a6 | Python Brasil 2019 | https://2019.pythonbrasil.org.br/ | S達o Paulo       |        | Brazil  | 2019-10-23 | 2019-10-29 |
| 3ae4f9 | PyCon Fr 2019      | https://www.pycon.fr/             | Bordeaux         |        | France  | 2019-10-31 | 2019-11-04 |
| 68bf57 | PyCon Sweden       | http://www.pycon.se/              | Stockholm        |        | Sweden  | 2019-10-31 | 2019-11-02 |

and more.

## Features

### Filters

<pre>
$ conrad show --cfp
</pre>

<pre>
$ conrad show --tag python
</pre>

<pre>
$ conrad show --name pycon
</pre>

<pre>
$ conrad show --location usa
</pre>

<pre>
$ conrad show --date ">= 2019-10-01" --date "<= 2020-01-01"
</pre>

### Reminders

Colored reminders.

<pre>
$ conrad remind -i 68bf57
$ conrad remind
</pre>

| name         | start_date | days_left                                       |
|--------------|------------|-------------------------------------------------|
| PyCon Sweden | 2019-10-31 | <span style="color:red">**2 days left!**</span> |

Add to `.bashrc`!

### Automated and community-driven updates

See contributing.

## Installation

### Using pip

You can simply use pip to install `conrad`:

<pre>
$ pip install conference-radar
</pre>

### From source code

Or you can clone the repo:

<pre>
$ git clone https://www.github.com/vinayak-mehta/conrad
</pre>

And install `conrad`:

<pre>
$ cd conrad
$ pip install .
</pre>

## Contributing

## Versioning

`conrad` uses [Semantic Versioning](https://semver.org/). For the available versions, see the tags on this repository.

## License

This project is licensed under the Apache License, see the [LICENSE](https://github.com/vinayak-mehta/conrad/blob/master/LICENSE) file for details.

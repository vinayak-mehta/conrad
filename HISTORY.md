Release History
===============

master
------

0.10.2 (2024-12-22)
-------------------

* Minor fixes.


0.10.1 (2021-08-01)
-------------------

* Show grid on table and hide state from output.

0.10.0 (2021-08-01)
-------------------

**Improvements**

* [#203](https://github.com/vinayak-mehta/conrad/pull/203) Add rich tables.

**Bugfixes**

* Fix reminder deletion bug on auto refresh.

0.9.1 (2021-06-24)
------------------

**Bugfixes**

* Fix `ImportError` caused by missing crawl requirements.

0.9.0 (2021-06-21)
------------------

**Improvements**

* Add `generate` and `run` commands to make crawler addition easy.

0.8.0 (2020-08-01)
------------------

**Bugfixes**

* New release because 0.7.1 doesn't show up as latest on PyPI.

0.7.1 (2020-08-01)
------------------

**Bugfixes**

* [#147](https://github.com/vinayak-mehta/conrad/issues/147) conrad show throws sqlalchemy.exc.OperationalError on upgrading to 0.7.0. [83f4e3b](https://github.com/vinayak-mehta/conrad/commit/83f4e3b4ebaa0be581418039dfcbb5ce89327194) by Vinayak Mehta.

0.7.0 (2020-08-01)
------------------

**Improvements**

* [#138](https://github.com/vinayak-mehta/conrad/issues/138) Add crawler for [Python events calendar](https://wiki.python.org/moin/PythonEventsCalendar). [#139](https://github.com/vinayak-mehta/conrad/pull/139) by Vinayak Mehta.
* [#142](https://github.com/vinayak-mehta/conrad/issues/142) Add support for multiple event schema versions. [#143](https://github.com/vinayak-mehta/conrad/pull/143) by Vinayak Mehta.
* [#37](https://github.com/vinayak-mehta/conrad/issues/37) Add nominatim geocoder util to standardize location. [#102](https://github.com/vinayak-mehta/conrad/pull/102) by [Sangarshanan](https://github.com/Sangarshanan).
* [#36](https://github.com/vinayak-mehta/conrad/issues/36) Add check for new conrad version. [#61](https://github.com/vinayak-mehta/conrad/pull/61) by [Abhi Baireddy](https://github.com/abhi-baireddy) and Vinayak Mehta.
* Add `--kind` filter for the `show` command. [#137](https://github.com/vinayak-mehta/conrad/pull/137) by Vinayak Mehta.
* [d3db41b](https://github.com/vinayak-mehta/conrad/commit/d3db41b777ab5a0b3d6734bbde33865842304854) Update .readthedocs.yml and remove requirements.txt
* Change auto-refresh interval from 1 day to 1 week.

0.6.2 (2020-07-28)
------------------

* Unpin requirements.

0.6.1 (2020-07-10)
------------------

* Add py38 trove classifier.

0.6.0 (2020-07-10)
------------------

**Improvements**

* [#46](https://github.com/vinayak-mehta/conrad/issues/46) Highlight events on conrad show for which reminders have been set. [225972d](https://github.com/vinayak-mehta/conrad/commit/225972d4ca505832cdcb2009b2c81cd0588d1532) by Vinayak Mehta.

0.5.0 (2020-07-09)
------------------

**Improvements**

* Add `--id` filter for the `show` command.
* Automatically set cfp flag to False if date has passed and don't import old events in the `import` command.

0.4.0 (2020-05-24)
------------------

**Improvements**

* Replace `.format` with f-strings! [5d5a917](https://github.com/vinayak-mehta/conrad/commit/5d5a9172231602427d7a959a7f3bbd3508d62a9a)
* Use [click.get_app_dir](https://github.com/vinayak-mehta/conrad/commit/6f2da95d85a7624568ae47cfe3348adca15629bf) for `CONRAD_HOME`.
* Fix days left [comparison operators](https://github.com/vinayak-mehta/conrad/commit/b4ffc0d54ded8dd9ae94ecd9202715512264583b).
* [#100](https://github.com/vinayak-mehta/conrad/issues/100) Use start date when cfp date has passed. [5d5a917](https://github.com/vinayak-mehta/conrad/commit/5d5a9172231602427d7a959a7f3bbd3508d62a9a) by Vinayak Mehta.
* [#85](https://github.com/vinayak-mehta/conrad/issues/85) Add crawler for awesome-italy-events. [#91](https://github.com/vinayak-mehta/conrad/pull/91) by Vinayak Mehta.

0.3.2 (2019-11-08)
------------------

* Json dump event tags.

0.3.1 (2019-11-08)
------------------

**Bugfixes**

* [#81](https://github.com/vinayak-mehta/conrad/issues/81) FileNotFoundError on first conrad show. [#82](https://github.com/vinayak-mehta/conrad/pull/82) by Vinayak Mehta.

0.3.0 (2019-11-08)
------------------

**Improvements**

* [#10](https://github.com/vinayak-mehta/conrad/issues/10), [#33](https://github.com/vinayak-mehta/conrad/issues/33), [#58](https://github.com/vinayak-mehta/conrad/issues/58) Add auto refresh. [#78](https://github.com/vinayak-mehta/conrad/pull/78) by Vinayak Mehta.
* Remove deprecated fields. [#77](https://github.com/vinayak-mehta/conrad/pull/77) by Vinayak Mehta.
* Update PyCon Crawler. [#73](https://github.com/vinayak-mehta/conrad/pull/73) by Vinayak Mehta.
* Enable GitHub Actions and Add BaseCrawler. [#70](https://github.com/vinayak-mehta/conrad/pull/70) by Vinayak Mehta.
* [#11](https://github.com/vinayak-mehta/conrad/issues/11) Upgrade duplicate finding logic with edit distance. [#68](https://github.com/vinayak-mehta/conrad/pull/68) by [Josemy Duarte](https://github.com/JosemyDuarte).
* [#15](https://github.com/vinayak-mehta/conrad/issues/15) Add PyData crawler. [#49](https://github.com/vinayak-mehta/conrad/pull/49) by [Cristhian Motoche](https://github.com/CristhianMotoche).

**Bugfixes**

* [#66](https://github.com/vinayak-mehta/conrad/pull/57) Initialize conrad context before executing remind. [#67](https://github.com/vinayak-mehta/conrad/pull/67) by [Josemy Duarte](https://github.com/JosemyDuarte).

**Documentation**

* Add docs for extending BaseCrawler.

0.2.0 (2019-10-31)
------------------

**Improvements**

* Remove prettytable and use cli_helpers. [#57](https://github.com/vinayak-mehta/conrad/pull/57) by Vinayak Mehta.
* [#44](https://github.com/vinayak-mehta/conrad/issues/44) Add id column to conrad remind output. [#47](https://github.com/vinayak-mehta/conrad/pull/47) by [Shalini Sreedhar](https://github.com/shalini-s).
* [#23](https://github.com/vinayak-mehta/conrad/issues/23) Add help text to all commands. [#30](https://github.com/vinayak-mehta/conrad/pull/30) by [Josemy Duarte](https://github.com/JosemyDuarte).
* Enable [continous quality](https://deepsource.io/gh/vinayak-mehta/conrad/?ref=repository-badge) by DeepSource.
* Add more conferences.

0.1.2 (2019-10-28)
------------------

**Improvements**

* Add more conferences. [#26](https://github.com/vinayak-mehta/conrad/pull/26) by [Sangarshanan](https://github.com/Sangarshanan).

**Bugfixes**

* [#8](https://github.com/vinayak-mehta/conrad/issues/8) Error in opening database before first refresh. [#14](https://github.com/vinayak-mehta/conrad/pull/14) by Vinayak Mehta.

0.1.1 (2019-10-28)
------------------

**Documentation**

* Add README fixes.

0.1.0 (2019-10-28)
------------------

* Birth!

Release History
===============

master
------

**Improvements**

* Use [click.get_app_dir](https://github.com/vinayak-mehta/conrad/commit/6f2da95d85a7624568ae47cfe3348adca15629bf) for `CONRAD_HOME`.
* Fix days left [comparison operators](https://github.com/vinayak-mehta/conrad/commit/b4ffc0d54ded8dd9ae94ecd9202715512264583b).
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

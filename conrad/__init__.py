# -*- coding: utf-8 -*-

import os

from click import get_app_dir

from .__version__ import __version__


CONRAD_HOME = get_app_dir("conrad")
SQL_ALCHEMY_CONN = "sqlite:///{}/conrad.db".format(CONRAD_HOME)


if not os.path.exists(CONRAD_HOME):
    os.makedirs(CONRAD_HOME)

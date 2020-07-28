# -*- coding: utf-8 -*-

import os

from click import get_app_dir

from .__version__ import __version__


CONRAD_HOME = get_app_dir("conrad")
SQL_ALCHEMY_CONN = f"sqlite:///{CONRAD_HOME}/conrad.db"

if not os.path.exists(CONRAD_HOME):
    os.makedirs(CONRAD_HOME)

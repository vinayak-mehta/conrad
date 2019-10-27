# -*- coding: utf-8 -*-

import os

from .__version__ import __version__


USER_HOME = os.path.expanduser("~")
CONRAD_HOME = os.path.join(USER_HOME, ".conrad")
SQL_ALCHEMY_CONN = "sqlite:///{}/conrad.db".format(CONRAD_HOME)

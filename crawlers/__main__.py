# -*- coding: utf-8 -*-

import sys
import inspect

from . import *


def main():
    crawler = [
        m[0]
        for m in inspect.getmembers(sys.modules[__name__], inspect.isclass)
        if m[1].__module__.startswith("crawlers") and m[0] == sys.argv[1]
    ]
    if len(crawler):
        filename = crawler[0].lower().replace("crawler", "")

        Crawler = eval(crawler[0])
        c = Crawler()
        c.get_events()
        c.export("data/{}_events.json".format(filename))
    else:
        print("Crawler not found!")


if __name__ == "__main__":
    main()

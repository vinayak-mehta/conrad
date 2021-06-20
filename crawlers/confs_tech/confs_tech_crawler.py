# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path

import git

from ..base import BaseCrawler


def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


class ConfsTechCrawler(BaseCrawler):
    def get_events(self):
        # Populate this list of events using your code
        events = []

        git.Git("/tmp").clone("https://github.com/tech-conferences/conference-data.git", depth=1)

        data_path = "/tmp/conference-data"
        mkdir(data_path)

        p = Path(data_path)
        years = ["2021", "2022"]
        conference_names = []

        for year in years:
            conferences_for_year_path = p / "conferences" / years[0]
            for tagfile in os.listdir(conferences_for_year_path):
                tag = tagfile.replace(".json", "")
                conferences_for_tag_for_year_path = conferences_for_year_path / tagfile

                with open(conferences_for_tag_for_year_path, "r") as f:
                    conferences = json.load(f)

                for conference in conferences:
                    conference_name = conference.get("name", "").lower()
                    if conference_name in conference_names:
                        continue
                    conference_names.append(conference_name)

                    city = conference.get("city")
                    country = conference.get("country")

                    cfp_end_date = conference.get("cfpEndDate") if conference.get("cfpEndDate") is not None else "1970-01-01"

                    conference_data = {
                        "name": conference.get("name"),
                        "url": conference.get("url"),
                        "city": city,
                        "state": conference.get("state"),
                        "country": country,
                        "location": ", ".join(
                            filter(lambda x: x is not None, [city, country])
                        ),
                        "cfp_open": False,
                        "cfp_end_date": cfp_end_date,
                        "start_date": conference.get("startDate"),
                        "end_date": conference.get("endDate"),
                        "source": "https://confs.tech",
                        "tags": [tag],
                        "kind": "conference",
                        "by": "bot",
                    }

                    self.events.append(conference_data)

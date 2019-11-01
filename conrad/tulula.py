import requests
import datetime
import base64
from collections import namedtuple
import logging
import time

# this agent is required to allow proper rate limiting.
TULULA_CONRAD_USER_AGENT = "conrad.api.v1"
TULULA_API_ENDPOINT = "https://tulu.la/api/public"
# rate limited by server, 5 requests per second
TULULA_TIME_BETWEEN_REQUESTS = 0.2
TULULA_MAX_PAGES = 100

TululaEvent = namedtuple(
    "TululaEvent",
    [
        "name",
        "date_start",
        "date_end",
        "cfp_date_start",
        "cfp_date_end",
        "cfp_is_active",
        "country",
        "state",
        "city",
        "tags",
        "source",
        "url",
        "kind",
    ],
)

logging.basicConfig(format="%(message)s", level=logging.INFO)


class Tulula:
    def __init__(
        self, user_agent=TULULA_CONRAD_USER_AGENT, api_endpoint=TULULA_API_ENDPOINT
    ):
        self.user_agent = user_agent
        self.api_endpoint = api_endpoint

    def get_new_events(self):
        now = datetime.date.today()
        has_next_page = True
        after = None
        i = 0
        events = []
        while has_next_page and i < TULULA_MAX_PAGES:
            logging.info("Get %d page", i + 1)
            data = self._get_page_data(now, after=after)
            if data is None:
                break
            page_info = data["events"]["pageInfo"]
            has_next_page, after = page_info["hasNextPage"], page_info["endCursor"]
            events.extend(self._parse_edges(data["events"]["edges"]))
            i += 1
            time.sleep(TULULA_TIME_BETWEEN_REQUESTS)
        logging.info("%d events has been fetched from tulu.la", len(events))
        return events

    def _get_page_data(self, date_from, after=None):
        operation = {
            "operationName": "QueryEventsList",
            "query": GQL_EVENT_QUERY,
            "variables": {
                "first": 25,
                "after": after,
                "filter": {"dateFrom": date_from.strftime("%Y-%m-%d")},
                "order": "ASC",
                "sort": "DATE_START",
                "searchView": "EVENTS_GRID",
            },
        }
        resp = requests.post(
            self.api_endpoint,
            json=operation,
            headers={
                "User-Agent": self.user_agent,
                "Accept-Language": "en-US,en;q=0.9",
            },
        )
        if resp.status_code not in [200, 422]:
            logging.error("Something went wrong. status_code %s", resp.status_code)
            return None

        response_data = resp.json()
        if "errors" in response_data:
            logging.error("%s", response_data)
            for err in response_data["errors"]:
                logging.error("Graphql error: %s", err["message"])

        return response_data["data"]

    def _parse_edges(self, edges):
        events = []
        for event_node in edges:
            node = event_node["node"]
            if not node["dateIsApproved"]:
                # an event is in maintenance mode
                continue
            events.append(
                TululaEvent(
                    name=node["name"],
                    date_start=node["dateStart"],
                    date_end=node["dateEnd"],
                    cfp_date_start=node["cfpDateStart"],
                    cfp_date_end=node["cfpDateEnd"],
                    cfp_is_active=node["cfpIsActive"],
                    country=node["venue"] and node["venue"]["country"],
                    state=node["venue"] and node["venue"]["state"],
                    city=node["venue"] and node["venue"]["city"],
                    tags=node["tags"],
                    source="https://tulu.la",
                    url=make_url(node["slug"], node["id"]),
                    kind="conference",
                )
            )
        return events


def base36encode(number):
    """
    Convert number to base36
    Based on https://github.com/tonyseek/python-base36/blob/master/base36.py
    :param number:
    :return: base36 encoded string
    """
    if not isinstance(number, (int,)):
        raise TypeError("number must be an integer")
    if number < 0:
        return "-" + base36encode(-number)

    alphabet, base36 = ["0123456789abcdefghijklmnopqrstuvwxyz", ""]

    while number:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return base36 or alphabet[0]

def make_url(slug, event_id):
    # base64("event:id") > base36(id)
    decoded_id = base64.b64decode(event_id)
    parts = decoded_id.split(b":")
    real_id = base36encode(int(parts[1]))
    return "https://tulu.la/events/{slug}-{id:0>6}".format(slug=slug, id=real_id)


GQL_EVENT_QUERY = """
query QueryEventsList($first: Int, $after: String, $filter: EventFilter,
                      $sort: EventSortField, $order: SortOrder,
                      $searchView: EventSearch) {
  events: events(range: {first: $first, after: $after},
                 filter: $filter, sortField: $sort,
                 sortOrder: $order, searchView: $searchView) {
    edges {
      node {
        id
        name
        slug
        dateStart
        dateEnd
        dateIsApproved
        cfpDateStart
        cfpDateEnd
        cfpIsActive
        venue {
          country
          state
          city
        }
        tags
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
"""

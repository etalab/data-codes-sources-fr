import csv
from distutils.util import strtobool

import requests


class SwhExists(object):
    SWH_FILE = "data/swh_exists.csv"

    def __init__(self):
        super(SwhExists, self).__init__()
        self.load_data()
        self.should_call_api = True

    def swh_url(self, origin_url):
        is_available = self.origin_available(origin_url)
        if is_available:
            return f"https://archive.softwareheritage.org/browse/origin/{origin_url}/directory/"
        elif is_available is None:
            return None
        elif not is_available:
            return False
        else:
            raise ValueError

    def load_data(self):
        self.data = {}
        with open(self.SWH_FILE) as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.store_origin_result(
                    row["origin_url"], bool(strtobool(row["is_available"]))
                )

    def save_data(self):
        with open(self.SWH_FILE, "w") as f:
            writer = csv.DictWriter(f, fieldnames=["origin_url", "is_available"])

            writer.writeheader()
            for origin_url, is_available in self.data.items():
                writer.writerow(
                    {"origin_url": origin_url, "is_available": is_available}
                )

    def store_origin_result(self, origin_url, is_available):
        self.data[origin_url] = is_available
        return is_available

    def origin_available(self, origin_url):
        if self.origin_exists(origin_url):
            return self.data[origin_url]
        if not self.should_call_api:
            return self.store_origin_result(origin_url, None)

        url = f"https://archive.softwareheritage.org/api/1/origin/git/url/{origin_url}"
        resp = requests.get(url, headers={"User-Agent": "etalab/data-codes-source-fr"})
        if resp.status_code == 200:
            return self.store_origin_result(origin_url, True)
        elif resp.status_code == 404:
            return self.store_origin_result(origin_url, False)
        elif resp.status_code == 429:
            self.should_call_api = False
            return self.store_origin_result(origin_url, None)
        else:
            resp.raise_for_status()

    def origin_exists(self, origin_url):
        return origin_url in self.data and self.data[origin_url] is not None

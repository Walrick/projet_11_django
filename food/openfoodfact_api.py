#!/usr/bin/python3
# -*- coding: utf8 -*-

import json
import time
import urllib.error
import urllib.parse
import urllib.request


class ApiOpenFoodFact:

    BASE_URL = "https://fr.openfoodfacts.org/"

    def query(self, url):

        print("url:", url)

        current_delay = 0.1  # Set the initial retry delay to 100ms.
        max_delay = 5  # Set the maximum retry delay to 5 seconds.

        while True:
            try:
                # Get the API response.
                response = urllib.request.urlopen(url)
            except urllib.error.URLError:
                pass  # Fall through to the retry loop.
            else:
                # If we didn't get an IOError then parse the result.
                result = json.load(response)
                return result

            if current_delay > max_delay:
                raise Exception("Too many retry attempts.")

            print("Waiting", current_delay, "seconds before retrying.")

            time.sleep(current_delay)
            current_delay *= 2  # Increase the delay each time we retry.

    def get_category(self):
        """
        Build category by query
        :return: {
        "tags" : [{"name": str, "url": str, "products": int,
         "known": int, "id": str},..],
        "count" : int
        }
        """

        # Join the parts of the URL together into one string.
        params = urllib.parse.urlencode(
            {
                'countries': 'France',
                'json': 1,
            }
        )

        url = f"{self.BASE_URL}categories/?{params}"

        response = self.query(url)
        return response

    def product_requests_by_category(self, category, page):
        """
        Build product by query in category
        :param category: str
        :param page: int
        :return: [{"product_name": str,
                "stores": str,
                "nutrition_grade_fr": str,
                "traces: str,
                "allergens": str,
                "url": str,
                ... }..]
                Look complete documentation in OpenFoodFact API
        """

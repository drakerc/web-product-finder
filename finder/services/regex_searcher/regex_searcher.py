import re
from typing import List

from finder.services.data_storage.data_storage import Product


class RegexSearcher:

    def find_matching_products(
            self,
            rule: str,
            data: List[Product],
            search_in: List[str]
    ) -> List[Product]:
        """
        Filters the data list to find products matching the provided regex
        :param rule: regex rule to be used when searching products, e.g. "^(?=.*Fanta).*"
        :param data: List of Product instances to be filtered with the regex
        :param search_in: List of Product attributes that need to be searched with regex,
         e.g. ['name', 'category']
        :return: Filtered list of Product instances
        """
        filtered_results = []
        for i in data:
            for searched_column in search_in:
                searched_data = getattr(i, searched_column)  # TODO: use EAFP principle?
                if searched_data and re.search(rule, searched_data):
                    filtered_results.append(i)
                    break
        return filtered_results

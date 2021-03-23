
class ItemsetCollection:
    """
    Class representing a set of item sets at each pass, k, of the algorithm.
    """

    def __init__(self, k):
        self.k = k       # iteration/pass number
        self.candidates_k = set()  # candidate item sets for level k
        self.large_k = set()  # item


class Itemset:
    """
    Class representing a single item set.
    """

    def __init__(self):
        self.items = set()
        self.support = 0

    def add_item(self, item):
        """
        Adds a new item to the item set.
        """
        self.items.add(item)

    def check_item(self, item):
        """
        Checks that an item is in the item set.
        """
        return True if item in self.items else False

    def incr_support(self):
        """
        Increments the support value for the item set by 1.
        """
        self.support += 1

    def sorted(self):
        """
        Returns a list of items in the itemset in lexographic order.
        """
        return list(self.items).sort()

class KItemsets:
    """
    Class representing a set of item sets at each pass, k, of the algorithm.
    """

    def __init__(self, k):
        self.k = k  # iteration/pass number
        self.item_sets = {}  # candidate item sets for level k; map of item set to count

from project3.itemsets import KItemsets
import itertools


class DataMiner:
    def __init__(self, data, min_supp, min_conf):
        self.data = data
        self.min_supp = min_supp
        self.min_conf = min_conf
        self.n_baskets = len(data)

    def compute_item_sets(self):
        """
        Computes all large item sets from a collection, given a previously specified
        minimum confidence and support.
        :return: A dictionary of large item set to support, for all large itemsets identified
        """
        # will contain a mapping of large itemsets to their count in data
        large_itemsets = {}

        # this result represents the L1 = {large 1-itemsets}, stored in collection_1.large_itemsets
        collection_1 = self._do_first_pass()

        # starting at k = 2, keep computing until we run out of large itemsets
        k = 2
        last_collection = collection_1
        while last_collection.items:
            # 1. add the prev large item sets to the global large item results dictionary
            large_itemsets.update(last_collection.items)

            # 2. generate the candidates for round k
            candidates_k = self._apriori_gen(k, last_collection.items)

            # 3. determine which candidates make it to the large candidate set for k
            collection_k = self._find_large_itemsets_for_k(candidates_k, k)

            # 4. keep going; we'll stop once there are no items returns in collection_k.items
            last_collection = collection_k
            k += 1

        return large_itemsets

    def _do_first_pass(self):
        """
        As a first pass of the algorithm, determine the L1 (large 1-item set) by finding
        each item in each row and adding the item to the candidate KItemsets if it is not already
        there. If the item has already been seen, then increment the count of the number of times
        that this item was seen.
        :return: Returns a new KItemset representing the collection of large/frequent 1-item sets.
        """
        candidates = KItemsets(1)
        for tup in self.data.itertuples():
            for el in tup:
                if el in candidates.items.keys():
                    candidates.items[frozenset({el})] += 1
                else:
                    candidates.items[frozenset({el})] = 1

        # iterate through the dataset and determine the support for each item, finalizing
        # the large set for this pass.
        collection_1 = KItemsets(1)
        for el, ct in candidates.items():
            support = ct / self.n_baskets
            if support > self.min_supp:
                collection_1.items[frozenset({el})] = ct

        return collection_1

    def _apriori_gen(self, k, collection_k_sub):
        """
        Takes large item sets from pass Lk-1 ('collection_k_sub') to generate candidate item sets
        for pass k. Takes the same approach as Agrawal & Srikant (1994), performing a join of
        Lk-1 with itself to return a superset of the set of all large k-itemsets (i.e., candidates).
        After the join, a prune step is used to delete item set c from c_k if any subset of c is
        not in k-1. Returns the new group of verified candidate itemsets for this iteration.

        Inspiration for how to perform join as part of candidate generation, using a nested
        for loop, was taken from:
        https://adataanalyst.com/machine-learning/apriori-algorithm-python-3-0/

        :param k: The iteration number of this candidate calculation
        :param collection_k_sub: KItemsets instance, the collection holding the L(k-1) large item set
        :return: new KItemsets containing candidates for iteration k
        """
        verified_candidates_k = KItemsets(k)
        possible_candidates = set()

        # list of lists corresponding to item sets from previous round
        prev_large_itemsets = collection_k_sub.items.keys()
        large_itemset_list = [list(itemset) for itemset in prev_large_itemsets]

        # perform the join of the Lk-1 set to get all candidates
        for i in range(len(large_itemset_list)):
            for j in range(i + 1, len(large_itemset_list)):
                p_set = large_itemset_list[i]
                q_set = large_itemset_list[j]
                if self._eligible_join(p_set, q_set, k):
                    possible_candidates.add(frozenset((sorted(p_set + q_set))))

        # "prune" the possible candidates for the final candidate set
        for candidate in possible_candidates:
            if self._candidate_should_be_pruned(candidate, prev_large_itemsets, k):
                continue
            verified_candidates_k.items[candidate] = 0

        return verified_candidates_k

    @staticmethod
    def _eligible_join(p, q, k):
        """
        Determines if, given two item sets, a join between the item sets should occur.
        Joins are only eligible if the item sets share the first k-2 elements and if the
        element at index k-2 in is "less than" the element at q.
        """
        if p[: k - 2] == q[: k - 2] and p[k - 2] < q[k - 2]:
            return True
        return False

    def _candidate_should_be_pruned(self, candidate, prev_large_itemsets, k):
        """
        Determines if the candidate itemset should be "pruned", i.e., disregarded because
        it contains a subset of elements that were not in the previous large itemsets from
        the k -1 iteration. Approach for determining itemsets from set taking from:
        https://www.geeksforgeeks.org/python-program-to-get-all-subsets-of-given-size-of-a-set/

        :param candidate: Candidate set of items
        :param prev_large_itemsets: Previous list of candidate sets
        :param k: The round that we are currently processing
        :return: True if the candidate should be pruned, False if it should be kept
        """
        sub_itemsets = self._find_subsets(candidate, k - 1)
        return (
            True
            if any(itemset in prev_large_itemsets for itemset in sub_itemsets)
            else False
        )

    def _find_large_itemsets_for_k(self, candidates_k, k):
        """
        Scan to find support for each of the candidates for k and add them to the large
        itemset for the new collection of large itemsets.
        """
        collection_k = KItemsets(k)

        for tup in self.data.itertuples():
            for subset in self._find_subsets(tup, k):

                # see if we found a record that contains this subset of tuples, so increment count
                if subset in candidates_k.items.keys():
                    collection_k.items[frozenset(subset)] += 1
                else:
                    collection_k.items[frozenset({subset})] = 1

        return collection_k

    @staticmethod
    def _find_subsets(s, n):
        """
        Finds all subsets of s with n elements. Approach for determining itemsets
        from set taking from:
        https://www.geeksforgeeks.org/python-program-to-get-all-subsets-of-given-size-of-a-set/
        :param s: the original set of elements
        :param n: number of elements in each subset
        :return: list of subsets with n elements
        """
        return list(map(set, itertools.combinations(s, n)))

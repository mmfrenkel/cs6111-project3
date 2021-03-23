from project3.itemsets import Itemset, ItemsetCollection
import pandas as pd


class DataMiner:

    def __init__(self, data, min_supp, min_conf):
        self.data = data
        self.min_supp = min_supp
        self.min_conf = min_conf
        self.collections = []

    def compute_item_sets(self):
        pass

    def first_pass(self):
        l1 = ItemsetCollection(1)

        # for each item in each row as an ItemSet to the Collection

        # iterate through the dataset and determine the support for each item, finalizing
        # the large set for this pass.
        pass

    def apriori_gen(self, l_k):
        """
        Takes large item sets from pass Lk-1 to generate candidate item sets for pass k, c_k.
        Takes the same approach as Agrawal & Srikant (1994), performing a join of Lk-1 with
        itself to return a superset of the set of all large k-itemsets (i.e., candidates). After
        the join, a prune step is used to delete itemset c from c_k if any subset of c is not in
        k-1.
        """
        pass

    def subset(self, c_k, dataset):
        """
        Scan to find support for each of the candidates Ck.
        """
        pass
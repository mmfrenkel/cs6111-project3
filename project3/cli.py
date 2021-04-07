from plumbum import cli, colors
from project3.data_miner import DataMiner
import pandas as pd
import textwrap

STARS = "***************************************************************************"
DEFAULT_DATASET = "./project3/data/restaurant_inspection_data_lim.csv"


class AssociativeRulesCli(cli.Application):

    PROGNAME = colors.bold
    VERSION = colors.yellow
    COLOR_GROUPS = {
        "Switches": colors.green,
        "Metaswitches": colors.bold & colors.yellow,
    }

    dataset_path = cli.SwitchAttr(
        ["-d", "--dataset"],
        argtype=str,
        default=DEFAULT_DATASET,
        help=f"Specify .csv file for processing. By default: {DEFAULT_DATASET}",
    )

    min_sup = cli.SwitchAttr(
        ["-s", "--minimum_support"],
        argtype=float,
        default=0.01,
        help="Specify a minimum support value (float, 0-1)",
    )

    min_conf = cli.SwitchAttr(
        ["-c", "--minimum_confidence"],
        argtype=float,
        default=0.2,
        help="Specify a minimum confidence value (float, 0-1)",
    )

    data = None  # until opened below

    def main(self):
        """
        Entry point into program, creates DataMiner instance and passes
        information to it.
        """
        self.data = self.open_csv_as_df()
        self.print_header()

        # find large itemsets
        miner = DataMiner(data=self.data, min_supp=self.min_sup, min_conf=self.min_conf)
        large_item_sets = miner.find_large_item_sets()
        self.report_large_itemsets(large_item_sets)
        high_conf_rules = miner.find_high_conf_rules(large_item_sets)
        self.report_high_conf_rules(high_conf_rules)

    def open_csv_as_df(self):
        """
        Reads a csv from file into a pandas data frame. Note that all values are
        loaded as the string datatype, even numeric columns.
        """
        if self.dataset_path[-4:] != ".csv":
            print("Please provide a valid .csv file")
            exit(1)

        try:
            return pd.read_csv(self.dataset_path, sep=",", dtype="string")
        except FileNotFoundError:
            print(
                "FileNotFound: Are you sure you provided the path to the .csv file"
                "correctly and that the file exists?"
            )
            exit(1)

    def print_header(self):
        print(STARS)
        print("                    ASSOCIATION RULE FINDER\n")
        print(f" * Dataset            : {self.dataset_path}")
        print(f" * Minimum Support    : {self.min_sup}")
        print(f" * Minimum Confidence : {self.min_conf}")
        print(STARS)

    def report_large_itemsets(self, item_sets):
        """
        Reports item set results back to user.
        """
        print(f"\n{STARS}")
        print(f"                  Large Itemsets Found ({len(item_sets)}):\n")
        for large_item_set, ct in item_sets.items():
            support = ct / len(self.data)
            print(textwrap.fill(f" * {list(large_item_set)}: {support:.1%}", 80))
        print(STARS)

    @staticmethod
    def report_high_conf_rules(association_rules):
        """
        Reports association rules that meet the confidence threshold back to the user.
        """
        n_result = len(association_rules)
        print(f"{STARS}")
        print(f"               High-Confidence Association Rules Found ({n_result}):")

        for i, rule in enumerate(association_rules):
            print(f"\nAssociation Rule #{i}")
            print(textwrap.fill(f"* Rule: {list(rule.lhs)} => {list(rule.rhs)} ", 80))
            print(f"* Metrics: (Conf: {rule.conf:.1%}, Sup: {rule.supp:.1%})")
        print(STARS)


if __name__ == "__main__":
    AssociativeRulesCli.run()

from plumbum import cli, colors
from project3.data_miner import DataMiner
import pandas as pd


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
        default="./project3/data/restaurant_inspection_data_adj.csv",
        help="Specify .csv file for processing. By default: "
        "./project3/data/restaurant_inspection_data.csv",
    )

    min_sup = cli.SwitchAttr(
        ["-s", "--minimum_support"],
        argtype=float,
        default=0.02,
        help="Specify a minimum support value (float, 0-1)",
    )

    min_conf = cli.SwitchAttr(
        ["-c", "--minimum_confidence"],
        argtype=float,
        default=0.6,
        help="Specify a minimum confidence value (float, 0-1)",
    )

    def main(self):
        """
        Entry point into program, creates DataMiner instance and passes
        information to it.
        """
        self.print_header()
        data = self.open_csv_as_df()
        data = data.head(10000)

        # find large itemsets
        miner = DataMiner(data=data, min_supp=self.min_sup, min_conf=self.min_conf)
        large_item_sets = miner.find_large_item_sets()
        self.report_large_itemsets(large_item_sets)
        high_conf_rules = miner.find_high_conf_rules(large_item_sets)
        self.report_high_conf_rules(high_conf_rules)

    def open_csv_as_df(self):
        """
        Reads a csv from file into a pandas data frame. Note that all values are
        loaded as the string datatype, even numeric columns.
        """
        try:
            return pd.read_csv(self.dataset_path, sep=",", dtype="string")
        except FileNotFoundError:
            print(
                "FileNotFound: Are you sure you provided the path to the .csv file"
                "correctly and that the file exists?"
            )
            exit(1)

    def print_header(self):
        print(
            "***************************************************************************"
        )
        print(
            "                        ASSOCIATION RULE FINDER                       \n"
        )
        print(f" * Dataset            : {self.dataset_path}")
        print(f" * Minimum Support    : {self.min_sup}")
        print(f" * Minimum Confidence : {self.min_conf}")
        print(
            "***************************************************************************"
        )

    @staticmethod
    def report_large_itemsets(item_sets):
        """
        Reports item set results back to user.
        """
        print(
            "\n***************************************************************************"
        )
        print(f"                  Large Itemsets Found ({len(item_sets)}): ")
        for large_item_set, support in item_sets.items():
            print(f" * {list(large_item_set)}: {support}")
        print(
            "***************************************************************************"
        )

    @staticmethod
    def report_high_conf_rules(association_rules):
        """
        Reports association rules that meet the confidence threshold back to the user.
        """
        ## DELETE LATER, THIS IS FOR LINH - for now the assumption is that the rules will be in a sorted list where each element in the list will be a Rule object - see rule.py for class info
        print(
            "\n***************************************************************************"
        )
        print(
            f"             High-Confidence Association Rules Found ({len(association_rules)}): "
        )
        for rule in association_rules:
            print(
                f" * {list(rule.lhs)} => {list(rule.rhs)} (Conf: {rule.conf:.1%}, Sup: {rule.supp:.1%})"
            )
        print(
            "***************************************************************************"
        )


if __name__ == "__main__":
    AssociativeRulesCli.run()

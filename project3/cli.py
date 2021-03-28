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

    dataset = cli.SwitchAttr(
        ["-d", "--dataset"],
        argtype=str,
        mandatory=False,
        help="Specify .csv file for processing. By default: .csv",
    )

    min_sup = cli.SwitchAttr(
        ["-s", "--minimum_support"],
        argtype=float,
        mandatory=True,
        help="Specify a minimum support value (float, 0-1)",
    )

    min_conf = cli.SwitchAttr(
        ["-c", "--minimum_confidence"],
        argtype=float,
        mandatory=True,
        help="Specify a minimum confidence value (float, 0-1)",
    )

    def main(self):
        """
        Entry point into program, creates DataMiner instance and passes
        information to it.
        """
        data = self.open_csv_as_df()

        miner = DataMiner(data=data, min_supp=self.min_sup, min_conf=self.min_conf)

        large_item_sets = miner.compute_item_sets()

    def open_csv_as_df(self):
        """
        Reads a csv from file into a pandas data frame.
        """
        try:
            return pd.read_csv(self.file_path)
        except FileNotFoundError:
            print(
                "FileNotFound: Are you sure you provided the path to the .csv file correctly?"
            )
            exit(1)

    def report_itemsets(self, item_sets):
        """
        Reports item set results back to user.
        """
        pass


if __name__ == "__main__":
    AssociativeRulesCli.run()

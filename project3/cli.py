from plumbum import cli, colors


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
        help="Specify .csv file for processing. By default: .csv"
    )

    min_sup = cli.SwitchAttr(
        ["-s", "--minimum_support"],
        argtype=float,
        mandatory=True,
        help="Specify a minimum support value (float, 0-1)"
    )

    min_conf = cli.SwitchAttr(
        ["-c", "--minimum_confidence"],
        argtype=float,
        mandatory=True,
        help="Specify a minimum confidence value (float, 0-1)"
    )

    def main(self):
        pass

if __name__ == "__main__":
    AssociativeRulesCli.run()


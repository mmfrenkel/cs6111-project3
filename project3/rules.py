class Rule:
    """
    Class representing all components needed to describe a rule
    """

    def __init__(self, lhs, rhs, supp, conf):
        self.lhs = lhs
        self.rhs = rhs
        self.supp = supp
        self.conf = conf

def make_adder(n):
    """Returns a functions that add n to the argument"""
    def adder(val):
        return val + n

    return adder

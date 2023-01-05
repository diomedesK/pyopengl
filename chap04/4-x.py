from numpy import arange

class Tester(object):
    """Workbench for testing"""
    def __init__(self):
        super(Tester, self).__init__()

    def main(self):

        for x in arange(-3.2, 3.2, 1.6):
            print(x)

Tester().main()

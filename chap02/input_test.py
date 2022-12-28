from core.Base import Base

class Executor(Base):
    """docstring for Executor"""
    def __init__(self):
        super(Executor, self).__init__()

    def initialize(self):
        pass
    
    def update(self):
        print(self.input.keyPressedList)
        pass


Executor().run()

__author__ = 'Soulweaver'


class UIObject:
    def __init__(self):
        # The main UIObject class specifies no functionality, it's simply used as a base class for all objects
        pass

    def input(self, event):
        # Handle a single event here
        pass

    def process(self):
        # Do by-tick events that are not dependent on input here
        pass

    def draw(self, screen):
        # Do draw events here
        pass

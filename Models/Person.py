class Person(object):
    """ A person has a name and a date to define their reservation """
    def init(self, name, date = None):
        self.name = name
        self.date = date

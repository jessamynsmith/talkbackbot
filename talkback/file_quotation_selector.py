from random import choice


class FileQuotationSelector(object):

    def __init__(self, settings):
        with open(settings.QUOTES_FILE) as quotes_file:
            self.quotes = quotes_file.readlines()

    def select(self):
        return choice(self.quotes).strip()

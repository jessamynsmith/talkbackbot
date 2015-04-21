import os
import unittest

from talkback.file_quotation_selector import FileQuotationSelector
import tests.test_settings


class TestFileQuotationSelector(unittest.TestCase):

    QUOTE1 = "A fool without fear is sometimes wiser than an angel with fear. ~ Nancy Astor"
    QUOTE2 = "You don't manage people, you manage things. You lead people. ~ Grace Hopper"

    def test_select(self):
        selector = FileQuotationSelector(tests.test_settings)
        selector.quotes = open(os.path.join(os.getcwd(), "tests/test_quotes.txt")).readlines()

        quote = selector.select()

        self.assertTrue(quote in (self.QUOTE1, self.QUOTE2),
                        "Got unexpected quote: '%s'" % quote)

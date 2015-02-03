import requests
import logging


class UrlQuotationSelector(object):

    def __init__(self, settings):
        self.quotes_url = settings.QUOTES_URL

    def select(self):
        quote = None
        response = requests.get(self.quotes_url)
        if response.status_code == 200:
            try:
                # TODO make this flexible based on format of returned json?
                quote_object = response.json()['objects'][0]
                quote = '%s ~ %s' % (quote_object['text'], quote_object['author']['name'])
            except ValueError:
                logging.error("Response from '%s' could not be decoded as JSON:\n%s"
                              % (self.quotes_url, response))
            except KeyError as e:
                logging.error("Response from '%s' did not contain field: %s\n%s"
                              % (self.quotes_url, e, response))

        else:
            logging.error("Got an error from '%s': %s\n%s"
                          % (self.quotes_url, response.status_code, response))
        return quote

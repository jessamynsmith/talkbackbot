import mock
import os
import types
import unittest

from talkback.bot import TalkBackBotFactory
import tests.test_settings


class TestTalkBackBot(unittest.TestCase):

    CHANNEL = "#testchannel"
    QUOTE = "Nobody minds having what is too good for them. ~ Jane Austen"
    USERNAME = "tester"

    def setUp(self):
        super(TestTalkBackBot, self).setUp()
        self.factory = TalkBackBotFactory(tests.test_settings)
        self.bot = self.factory.buildProtocol(None)
        self.bot.msg = mock.MagicMock()
        self.bot.join = mock.MagicMock()

    def test_init_no_quotes_source(self):
        settings = types.ModuleType('test_url_settings')
        settings.CHANNEL = "#inane"

        try:
            TalkBackBotFactory(settings)
            self.fail("Should not be able to initialize bot with no QUOTES_FILE or QUOTES_URL")
        except AttributeError as e:
            self.assertEqual('Must specify either QUOTES_URL or QUOTES_FILE in settings', str(e))

    def test_init_with_file(self):
        settings = types.ModuleType('test_url_settings')
        settings.CHANNEL = "#inane"
        settings.QUOTES_FILE = os.path.join(os.getcwd(), "tests/test_quotes.txt")

        bot = TalkBackBotFactory(settings)

        expected = [
            ' A fool without fear is sometimes wiser than an angel with fear. ~ Nancy Astor\n',
            "    You don't manage people, you manage things. You lead people. ~ Grace Hopper"
        ]
        self.assertEqual(expected, bot.quotation.quotes)

    def test_init_with_url(self):
        settings = types.ModuleType('test_url_settings')
        settings.CHANNEL = "#inane"
        settings.QUOTES_URL = "https://example.com/api/v2/quotations/?limit=1"

        bot = TalkBackBotFactory(settings)

        self.assertEqual("https://example.com/api/v2/quotations/?limit=1", bot.quotation.quotes_url)

    @mock.patch('twisted.words.protocols.irc.IRCClient.connectionMade')
    @mock.patch('logging.info')
    def test_connectionMade(self, mock_log_info, mock_made):
        self.bot.connectionMade()

        mock_made.assert_called_once_with(self.bot)
        mock_log_info.assert_called_once_with('connectionMade')

    @mock.patch('twisted.words.protocols.irc.IRCClient.connectionLost')
    @mock.patch('logging.info')
    def test_connectionLost(self, mock_log_info, mock_lost):
        self.bot.connectionLost('bad stuff')

        mock_lost.assert_called_once_with(self.bot, 'bad stuff')
        mock_log_info.assert_called_once_with('connectionLost')

    @mock.patch('logging.info')
    def test_signedOn(self, mock_log_info):
        self.bot.signedOn()

        self.bot.join.assert_called_once_with('#test')
        mock_log_info.assert_called_once_with('Signed on')

    @mock.patch('logging.info')
    def test_joined(self, mock_log_info):
        self.bot.joined(self.CHANNEL)
        mock_log_info.assert_called_once_with('[shesaidbot has joined #test]')

    def test_privmsg__no_trigger(self):
        """Shouldn't send a quote if message does not match trigger"""
        self.bot.privmsg(self.USERNAME, self.CHANNEL, "hi")
        self.assertFalse(self.bot.msg.called)

    def test_privmsg__with_trigger(self):
        """Should send a quote if message matches trigger"""
        self.bot.privmsg(self.USERNAME, self.CHANNEL, "twss")
        self.bot.msg.assert_called_with(self.CHANNEL, self.QUOTE)

    def test_privmsg__private_message(self):
        """ For private messages, should send quote directly to user """
        self.bot.privmsg(self.USERNAME, tests.test_settings.NICKNAME, "hi")
        self.bot.msg.assert_called_with(self.USERNAME, self.QUOTE)

    def test_privmsg__private_message_truncated_nickname(self):
        """ Send quote directly to user even if name is truncated """
        self.bot.privmsg(self.USERNAME, tests.test_settings.NICKNAME[:-2], "hi")
        self.bot.msg.assert_called_with(self.USERNAME, self.QUOTE)

    def test_privmsg__private_message_alternate_nickname(self):
        """ Send quote directly to user even if using alternate nickname """
        self.bot.privmsg(self.USERNAME, tests.test_settings.NICKNAME + '_', "hi")
        self.bot.msg.assert_called_with(self.USERNAME, self.QUOTE)

    @mock.patch('logging.info')
    def test_clientConnectionLost(self, mock_log_info):
        mock_connector = mock.MagicMock(connect=mock.MagicMock())

        self.factory.clientConnectionLost(mock_connector, 'error occurred')

        mock_connector.connect.assert_called_once_with()
        mock_log_info.assert_called_once_with('connection lost, reconnecting')

    @mock.patch('logging.info')
    def test_clientConnectionFailed(self, mock_log_info):
        mock_connector = mock.MagicMock()

        self.factory.clientConnectionFailed(mock_connector, 'error occurred')

        mock_connector.connect.assert_called_once_with()
        mock_log_info.assert_called_once_with('connection failed: error occurred')

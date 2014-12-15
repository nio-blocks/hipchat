from unittest.mock import patch, MagicMock
from ..hipchat_block import HipChat
from nio.util.support.block_test_case import NIOBlockTestCase
from nio.common.signal.base import Signal
from nio.modules.threading import Event


class HipChatTest(HipChat):

    def __init__(self, event):
        super().__init__()
        self._event = event

    def configure(self, context):
        super().configure(context)
        self._event.set()


class TestHipChatBlock(NIOBlockTestCase):
    def get_test_modules(self):
        return self.ServiceDefaultModules + ['persistence']
    
    def setUp(self):
        super().setUp()
        self.signals = [
            Signal({'val': 1})
        ]

    @patch('hipchat.HipChat.__init__', return_value=None)
    @patch('hipchat.HipChat.message_room')
    @patch('hipchat.HipChat.find_room', return_value = {'room_id': 23})
    def test_deliver_messages(self, mock_find, mock_msg, mock_constr):
        e = Event()
        blk = HipChatTest(e)
        self.configure_block(blk, {
            "token": "somebogustoken",
            "message": "The value: {{$val}}",
            "room_name": "TheRoom",
            "sender": "Joe",
        })

        # confirm that the room id was recorded
        self.assertEqual(blk.persistence.load("TheRoom"), 23)

        # avoid saving to disk
        blk.persistence.save = MagicMock()
        
        blk.start()
        blk.process_signals(self.signals)
        mock_msg.assert_called_with(23, 'Joe', 'The value: 1',
                                    color='', notify=False)
        blk.stop()

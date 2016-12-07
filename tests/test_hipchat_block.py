from unittest.mock import patch, MagicMock
from ..hipchat_block import HipChat
from nio.testing.block_test_case import NIOBlockTestCase
from nio.signal.base import Signal


class TestHipChatBlock(NIOBlockTestCase):

    @patch('hipchat.HipChat.__init__', return_value=None)
    @patch('hipchat.HipChat.message_room')
    @patch('hipchat.HipChat.find_room', return_value={'room_id': 23})
    def test_deliver_messages(self, mock_find, mock_msg, mock_constr):
        blk = HipChat()
        self.configure_block(blk, {
            "token": "somebogustoken",
            "message": "The value: {{$val}}",
            "room_name": "TheRoom",
            "sender": "Joe",
        })

        blk.start()
        blk.process_signals([Signal({'val': 1})])
        mock_msg.assert_called_with(23, 'Joe', 'The value: 1',
                                    color='', notify=False)
        blk.stop()

from unittest.mock import patch, MagicMock
from ..hipchat_block import HipChat
from nioext.util.support.block_test_case import NIOExtBlockTestCase
from nio.common.signal.base import Signal


class TestHipChatBlock(NIOExtBlockTestCase):

    def get_test_modules(self):
        return super().get_test_modules() + ['persistence']

    def get_module_config_persistence(self):
        """ Make sure we use file persistence """
        return {'persistence': 'file'}

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

        # avoid saving to disk
        blk.persistence.save = MagicMock()

        # confirm that the room id was recorded
        self.assertEqual(blk.persistence.load("TheRoom"), 23)

        blk.start()
        blk.process_signals([Signal({'val': 1})])
        mock_msg.assert_called_with(23, 'Joe', 'The value: 1',
                                    color='', notify=False)
        blk.stop()

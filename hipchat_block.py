from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.common.command import command
from nio.metadata.properties import BoolProperty, SelectProperty, \
    StringProperty, ExpressionProperty

from hipchat import HipChat as HC
from enum import Enum


class Color(Enum):
    NONE = ''
    YELLOW = "yellow"
    RED = "red"
    GREEN = "green"
    PURPLE = "purple"
    GRAY = "gray"
    RANDOM = "random"


@command('list_rooms')
@command('list_users')
@Discoverable(DiscoverableType.block)
class HipChat(Block):

    """ A block for sending messages to a HipChat room.

    Properties:
        token (str): Auth token (distributed by account admin)
        message (expr): Message contents.
        room_name (str): The plaintext name of the target HipChat room.
        sender (expr): Sender name to attach to the message.
        message_color (enum): The color of the message.
        notify (bool): Whether or not to send a notification to the members
            of the room when the message arrives.

    """
    token = StringProperty(title="API Token", default="[[HIPCHAT_TOKEN]]")
    message = ExpressionProperty(title="Message contents", default='')
    room_name = StringProperty(title="Room Name", default='')
    sender = ExpressionProperty(title="Sender Name", default='')
    message_color = SelectProperty(
        Color, title="Message Color", default=Color.NONE)
    notify = BoolProperty(title="Notify Users in Room", default=False)

    def __init__(self):
        super().__init__()
        self.hipster = None
        self.room_id = None

    def configure(self, context):
        super().configure(context)
        self.hipster = HC(token=self.token)
        self.room_id = self.persistence.load(self.room_name)
        if self.room_id is None:
            room = self.hipster.find_room(self.room_name)
            if room is None:
                self._logger.error(
                    "Hipchat room '{}' does not exist".format(self.room_name)
                )
            else:
                self.room_id = room.get('room_id')

        self.persistence.store(self.room_name, self.room_id)

    def start(self):
        super().start()
        self.persistence.save()

    def process_signals(self, signals):
        for signal in signals:
            msg = self.message(signal)
            sender = self.sender(signal)
            try:
                self.hipster.message_room(self.room_id, sender, msg,
                                          color=self.message_color.value,
                                          notify=self.notify)
            except Exception as e:
                self._logger.error(
                    "Failed to message HipChat room {}: {}".format(
                        self.room_name, str(e))
                )

    def list_rooms(self):
        return self.hipster.list_rooms()

    def list_users(self):
        return self.hipster.list_users()
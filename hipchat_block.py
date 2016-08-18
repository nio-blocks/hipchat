from nio.block.base import Block
from nio.util.discovery import discoverable
from nio.command import command
from nio.properties import BoolProperty, SelectProperty, \
    StringProperty, Property
from nio.block.mixins.persistence.persistence import Persistence

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
@discoverable
class HipChat(Persistence, Block):

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
    message = Property(title="Message contents", default='')
    room_name = StringProperty(title="Room Name", default='')
    sender = Property(title="Sender Name", default='')
    message_color = SelectProperty(
        Color, title="Message Color", default=Color.NONE)
    notify = BoolProperty(title="Notify Users in Room", default=False)

    def __init__(self):
        super().__init__()
        self.hipster = None
        self.room_id = None

    def configure(self, context):
        super().configure(context)
        self.hipster = HC(token=self.token())
        if self.room_id is None:
            room = self.hipster.find_room(self.room_name())
            if room is None:
                self.logger.error(
                    "Hipchat room '{}' does not exist".format(self.room_name())
                )
            else:
                self.room_id = room.get('room_id')

    def start(self):
        super().start()

    def process_signals(self, signals):
        for signal in signals:
            msg = self.message(signal)
            sender = self.sender(signal)
            try:
                self.hipster.message_room(self.room_id, sender, msg,
                                          color=self.message_color().value,
                                          notify=self.notify())
            except Exception as e:
                self.logger.error(
                    "Failed to message HipChat room {}: {}".format(
                        self.room_name(), str(e))
                )

    def persisted_values(self):
        """Persist room_name using block mixin."""
        return ["room_id"]

    def list_rooms(self):
        return self.hipster.list_rooms()

    def list_users(self):
        return self.hipster.list_users()

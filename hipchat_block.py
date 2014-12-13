from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.common.command import command
from nio.metadata.properties.holder import PropertyHolder
from nio.metadata.properties.list import ListProperty
from nio.metadata.properties.bool import BoolProperty
from nio.metadata.properties.object import ObjectProperty
from nio.metadata.properties.select import SelectProperty
from nio.metadata.properties.string import StringProperty
from nio.metadata.properties.Expression import ExpressionProperty

from python-simple-hipchat import HipChat as HC
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

    token = Stringproperty(title="API Token", default="[HIPCHAT_TOKEN]")
    message = ExpresisonProperty(title="Message contents", default='')
    room_id = IntProperty(title="Numeric Room ID", allow_none=True)
    room_name = StringProperty(title="Room Name", default='')
    from_name = StringProperty(title="Sender Name", default='')
    message_color = SelectProperty(Color, title="Message Color", default=Color.NONE)
    notify = BoolProperty(title="Notify Users in Room", default=False)

    def __init__(self):
        super().__init__()
        self.hipster = None

    def configure(self, context):
        super().configure(context)
        self.hipster = HC(token=self.token)
        if self.room_id is None:
            self.room_id = self.hipster.find_room(self.room_name)

    def process_signals(self, signals):
        for signal in signals:
            msg = self.message(signal)
            self.hipster.message_room(self.room_id, self.from_name, msg,
                                      color=self.message_color.value,
                                      notify=self.notify)

    def list_rooms(self):
        return self.hipster.list_rooms()

    def list_users(self):
        return self.hipster.list_users()

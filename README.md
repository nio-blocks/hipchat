HipChat
=======
Send messages to a HipChat room.

Properties
----------
- **backup_interval**: How often to save persisted data.
- **load_from_persistence**: If true, the block’s state will be saved at a block stoppage and reloaded upon restart.
- **message**: Message to post to HipChati.
- **message_color**: The message will appear with this color.
- **notify**: Whether or not to notify the occupants of the room when the message arrives.
- **room_name**: The plaintext name of the target HipChat room.
- **sender**: The sender name to associate with the message.
- **token**: Authentication token for HipChat account.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
None

Commands
--------
- **list_rooms**: Get rooms associated with the HipChat account.
- **list_users**: Get users associated with the HipChat account.

Dependencies
------------
- [python-simple-hipchat](https://pypi.python.org/pypi/python-simple-hipchat)

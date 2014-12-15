HipChat
=======

Block for sending messages to a HipChat room

Properties
----------

-   **token** (str): Authentication token for HipChat account.
-   **message** (expr): Expression property for the message.
-   **room_name** (str): The plaintext name of the target HipChat room.
-   **sender** (expr): The sender name to associate with the message.
-   **message_color** (enum): The message will appear with this color.
-   **notify** (bool): Whether or not to notify the occupants of the room when the message arrives.

Dependencies
------------

-   [python-simple-hipchat](https://pypi.python.org/pypi/python-simple-hipchat/0.3.2)


Commands
--------

-   **list_rooms**: Return a list of the rooms associated with the Auth token provided.
-   **list_users**: Return a list of the users associated with the Auth token provided.

Input
-----
Any list of signals. Messages are constructed by evaluating the *HipChat.message* against each signal.

Output
------
None

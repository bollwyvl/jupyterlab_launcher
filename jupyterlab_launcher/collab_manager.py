from traitlets.config import LoggingConfigurable
from uuid import uuid4
from collections import OrderedDict


class CollaborationManager(LoggingConfigurable):
    def __init__(self):
        self._sockets = []
        self._messages = OrderedDict()

    def register_socket(self, socket):
        self._sockets.append(socket)

    def unregister_socket(self, socket):
        self._sockets.remove(socket)

    def on_message(self, message, sender):
        self._save_message(message)
        self._broadcast(message, sender)

    def get_message_id(self, message):
        # TODO needs real things
        return str(uuid4())

    def _save_message(self, message):
        msg_id = self.get_message_id(message)
        self._messages[msg_id] = message

    def _broadcast(self, message, sender):
        # TODO SAVE
        for socket in self._sockets:
            if sender != socket:
                socket.write_message(message)

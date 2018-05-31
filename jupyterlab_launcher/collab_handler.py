from notebook.base.zmqhandlers import WebSocketMixin, WebSocketHandler
from notebook.base.handlers import IPythonHandler

TEST_PAGE = """
<!doctype html>
<body>
  <button>message</button>

  <script>
    var ws_url = 'ws://' + window.location.host + '/lab/collab/';
    var exampleSocket = new WebSocket(ws_url);

    exampleSocket.onopen = function(event){
      console.log("openened", event);
    }

    exampleSocket.onmessage = function(event){
      console.log("got message", event);
    }

    exampleSocket.onclose = function(event){
      console.log("got CLOSED", event);
    }

    document.querySelector("button").addEventListener("click", function(){
      exampleSocket.send(JSON.stringify({"woo": "Haa"}));
    });
  </script>
</body>
"""


class CollaborationTestHandler(IPythonHandler):
    # TODO: delete
    def __init__(self, *args, **kwargs):
        super(CollaborationTestHandler, self).__init__(*args, **kwargs)

    def get(self):
        self.write(TEST_PAGE)


# TODO: do we need this
# class CollaborationSocketactory(): ...


class CollaborationSocketHandler(WebSocketMixin, WebSocketHandler):
    # TODO fix
    allow_origin = "*"

    def initialize(self, collab_manager=None, *args, **kwargs):
        super(CollaborationSocketHandler, self).initialize(*args, **kwargs)
        self.collab_manager = collab_manager

    def open(self):
        print("WebSocket opened")
        self.collab_manager.register_socket(self)

    def on_message(self, message):
        self.collab_manager.on_message(message, self)

    def on_close(self):
        print("WebSocket closed")
        self.collab_manager.unregister_socket(self)

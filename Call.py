import server_main
import client
import fire

class Chat_Room:
    def Start_Server(self, ACTIVATE_SERVER):
        if ACTIVATE_SERVER == "activate":
            return server_main.core()
        else:
            return "Run python3 Call.py - -- --help for more information about commands"

    def Start_Client(self, ACTIVATE_CLIENT):
        if ACTIVATE_CLIENT == "activate":
            return client.Client()
        else:
            return "Run python3 Call.py - -- --help for more information about commands"


if __name__ == "__main__":
    fire.Fire(Chat_Room)
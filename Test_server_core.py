import unittest
import socket
from unittest.mock import patch
from loading_modules import loading_modules
from server_core import low_interface_of_server
import sys
from io import StringIO

class TestServerCore(unittest.TestCase):

    def test_CoreServer_ImpModules(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        core_server = low_interface_of_server(server, '', 7122, test=True)
        assert isinstance(core_server.modules, loading_modules)
    
    def test_CoreServer_EnlistPublicUsers(self):
        core_server = low_interface_of_server  
        print_output = []
        save_stdout = sys.stdout
        result = StringIO()
        sys.stdout = result
        fake_public_names=["user1", "user2", "user3", "user4", "user5"]
        core_server.Enlist_Public_Users(core_server,fake_public_names)
        sys.stdout = save_stdout
        print_output.append(result.getvalue())
        print_output = print_output[0]
        Enlist_Public_Users_MethodOutput = print_output.split('\n')
        self.assertEqual(Enlist_Public_Users_MethodOutput[:-1], fake_public_names)
    
    def test_CoreServer_PublicLists(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        core_server = low_interface_of_server(server, '', 7124, test=True)
        self.assertEqual(core_server.Public_clients, [] and core_server.Public_names, [])

    def test_CoreServer_PrivateChatMethod(self):
        with patch('server_core.low_interface_of_server.Private_Chat') as private_chat:
           private_chat.return_value = None
        self.assertIsNone(private_chat())
    
    def test_CoreServer_PrivateLists(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        core_server = low_interface_of_server(server, '', 7125, test=True)
        self.assertEqual(core_server.Private_clients, [] and core_server.Private_names, [])    
    
    def test_CoreServer_BroadcastMethod(self):
        sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        core_server = low_interface_of_server(sender, '', 7126, test=True)
        self.assertEqual(core_server.broadcast("message".encode("ascii"),sender,[]), None)

    def test_CoreServer_PrivateChatReciever(self):
        sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        reciever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        core_server = low_interface_of_server
        self.assertEqual(core_server.Private_chat_Reciever(core_server,sender, reciever), None)
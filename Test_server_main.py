import unittest
from  server_main import server, core
import socket
from unittest.mock import patch
from loading_modules import loading_modules
from  server_core import low_interface_of_server

class TestServerMain(unittest.TestCase):

    def test_Server_Necessary_ImportedModules(self):
        initialize_server = server(test_port=5553)
        assert isinstance(initialize_server.Modules, loading_modules)
    
    def test_Server_Port_Check(self):
        initialize_server = server(test_port=5553)
        self.assertEqual(initialize_server.PORT, 5553)

    def test_Server_Socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        initialize_server = server(test_port=5553)
        self.assertEqual(type(initialize_server.server), type(sock))

    def test_Server_StartMethod(self):
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        core_server = low_interface_of_server(sock ,'' , 3456, test=True)
        with patch('server_main.server.start') as coreserver:
            coreserver.return_value=core_server
        self.assertEqual(coreserver(), core_server)
    
    def test_Server_StopMethod(self):
        self.assertEqual(server.stop(server), None)

    def test_Server_ExitMethod(self):
        self.assertEqual(server.exit(server), None)

def test_CoreMethod():
    with patch('server_main.core') as core:
        core.return_value = None
    assert core() is None


            
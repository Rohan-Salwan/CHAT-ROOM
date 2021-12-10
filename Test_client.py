from client import Client
import unittest
from  server_core import low_interface_of_server
import socket
from unittest.mock import patch


class TestClient(unittest.TestCase):

    def test_Client_passing_key_worlds_dic(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        main_server = low_interface_of_server(server, '', 8844, test = True)
        user = Client(test_port = 8844, test_name = 'vishu')
        self.assertEqual(user.passing_key_words, {'/PRIVATECHAT': "", '/YES': ""})
    
    def test_Client_breaking_keywords_dic(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main_server = low_interface_of_server(server, '', 8844, test=True)
        user = Client(test_port = 8844, test_name = 'vishu')
        self.assertEqual(user.breaking_keywords, {'KICKED': ""})
    
    def test_Client_socket(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main_server = low_interface_of_server(server, '', 8844, test = True)
        user = Client(test_port = 8844, test_name = 'vishu')
        self.assertEqual(type(server), type(user.sock))
    
    def test_Client_Obtaining_UserInput_method(self):
        with patch('client.Client.Obtaining_UserInput') as userIO:
            userIO.return_value = 2222
        self.assertEqual(userIO(), 2222)
    
    def test_reciever_returnVal_and_socketClosemethod(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main_server = low_interface_of_server(server, '', 8844, test = True)
        user = Client(test_port = 8844, test_name = 'vishu')
        return_val = user.reciever(server)
        self.assertEqual(return_val, None)

    def test_sender(self):
        with patch('client.Client.sender') as sender:
            sender.return_value = None
        self.assertEqual(sender(), None)


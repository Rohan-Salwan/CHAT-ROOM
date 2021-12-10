class loading_modules:    
    def __init__(self):
    
        # all necessary modules are going to be import.

        # logging module is going to be import to keep logs of error or any information which can be useful in debugging.

        try:
            import logging
            self.logging = logging
            self.logging.basicConfig(filename = 'logs.txt', level = logging.DEBUG,
                format = '%(asctime)s %(levelname)s %(name)s %(message)s')
            self.logger = self.logging.getLogger(__name__)
        except Exception as e:
            print('logging module import error')

        # threading module is going to be import to speed up server service.
        try:
            import threading
            self.threading = threading
        except Exception as e:
            self.logger.error(e)
            print('threading module Import error')

        # socket module is going to be import for connection establishment and communication.
        try:
            import socket
            self.socket = socket
        except Exception as e:
            self.logger.error(e)
            print('socket module Import error')

        # os module is going to be import for making directories and changing location and searching directories and accessing files.
        try: 
            import os
            self.os = os
        except Exception as e:
            self.logger.error(e)
            print('os module Import error')

        # sys Module is going to be import for system operations
        try:
            import sys
            self.sys = sys
        except Exception as e:
            self.logger.error(e)
            print('sys module Import error')

        # time module is going to be import for calculating time and displaying time and for other stuff too.
        try:
            import time
            self.time = time
        except Exception as e:
            self.logger.error(e)
            print('time module Import error')
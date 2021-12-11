# CHAT-ROOM
CHAT-ROOM is a messaging application and it has two main modes first one is Public-Chat and 
second one is Private-Chat so user can go with the specific choice. Moreover, User can switch 
mode at any time by using some specific commands so features are very easy accessible. 
In addition, on Server-Side there are some privileges like first one is kick so server side 
person can kick anyone at anytime and second one is blocking so server side mantainer can 
block anyone. Right now it can only operate by command line but GUI is also coming soon.

Installing
----------

Use Clone Command To Install CHAT-ROOM:

    $ git clone https://github.com/Rohan-Salwan/CHAT-ROOM.git

For Installing Dependencies:

    $ pip install -r requirements.txt

Activate Chat-Room
-------------

For Starting Server:

    $ python3 Call.py Start_Server activate

For Starting Client:

    $ python3 Call.py Start_Client activate

For Help:

    $ python3 Call.py - -- --help

CHAT-Room Options
-----------------

To Switch Private Chat:
    <pre>/PRIVATECHAT</pre>

To Exit Chat-Room:
    <pre>/EXIT</pre>

To Block User:
    <pre>/BLOCK</pre>

To Accept Chat Request:
    <pre>/YES</pre>

Contribution
------------

Firstly Activate Environment:

    $ source Env/bin/activate

Secondly Install Dependencies:

    $ pip install -r requirements.txt

Next Step:
<pre>Always Import Modules In Loading_modules.py</pre>

<pre>Always Use Logger For Debugging Purposes</pre>

Always Run Tests:

    $ pytest Test_server_main.py
    $ pytest Test_Server_core.py
    $ pytest Test_client.py

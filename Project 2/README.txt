=========================================
Project 2 for EE450, USC 2016 Spring
=========================================


1.AUTHOR: ZHE JIAO   zjiao@usc.edu

2.BUILD: 
	No code to compile. Use Python2.7 or Python3.5 to run the peerchat.py.

3.RUN:
	
	The code can run based on the Pycharm IDE and other Python development environment.
	
	When the code runs, we connect to the registration server and register with the name server.
	
	Then we input the command ’ids’ to pull down the registry.

	Next, we can execute ‘msg’ to send messages to others. If we have an address in the registry, we can directly sent to that ID. If not, we will forward the packet to the first three IDs in the registry.

	Besides, we can broadcast messages to all IDs in my registry by using the command ‘all’. First, we input ‘all’ and Enter. Then, we input the message.
	
	

4.BUGS:

       1.When using command ‘all’ to broadcast messages, there is an error like ”socket.error: [Errno 65] No route to host” which would stop my code. But this error does not happen always.

	2.When receiving messages which are not addressed to me, I will forward the packet to first three IDs in my registry.  But there is no response several times when I receiving messages that I need to forward.
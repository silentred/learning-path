#!/usr/bin/python

# import socket
# s = socket.socket()

# host = socket.gethostname()
# port = 8808
# s.bind((host, port))
# s.listen(5)
# while True:
# 	c, addr = s.accept()
# 	print 'Got connection from ', addr
# 	c.send('Thank you for connecting')
# 	c.close()


from SocketServer import TCPServer, ForkingMixIn, StreamRequestHandler, ThreadingMixIn

# use fork
#class Server(ForkingMixIn, TCPServer):pass
# use thread
class Server(ThreadingMixIn, TCPServer):pass

class Handler(StreamRequestHandler):
	def handle(self):
		addr = self.request.getpeername()
		print 'Got connection from ', addr
		self.wfile.write('Thank you')
s = Server(('', 8808), Handler)
s.serve_forever()




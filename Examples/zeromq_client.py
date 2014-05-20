import time
import zmq


def client(port="5556", req=5):
    context = zmq.Context()
    print "Connecting to server with ports %s" % port
    socket = context.socket(zmq.REQ)
    socket.connect ("tcp://localhost:%s" % port)
    for request in range (req):
        print "Sending request ", request,"..."
        socket.send ("Hello")
        message = socket.recv()
        print "Received reply ", request, "[", message, "]"
        time.sleep (1)

if __name__ == "__main__":
    client()
import zmq


def server(port='5556', req=5):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:%s' % port)
    print 'Running server on port: ', port
    # serves only 5 request and dies
    for reqnum in range(req):
        # Wait for next request from client
        message = socket.recv()
        print 'Received request #%s: %s' % (reqnum, message)
        socket.send('World from %s' % port)

if __name__ == "__main__":
    server()
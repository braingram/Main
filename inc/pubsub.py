import pickle
from socket import *
import threading
import StringIO
import time

class Publisher:
    def __init__( self, port ):
        # Start the publishing server on specified TCP port
        self.port         = port
        self.sock         = None
        self.conn         = None
        self.serverThread = None
        self.restartflag  = 0

        # Catalog lists all the data offered by the publisher
        self.catalog = {}
        # Subscriptions is a list of all the offerings the client is subscribing to
        self.subscriptions = []

    def addToCatalog( self, name, callback ):
        self.catalog[name] = callback

    def start( self ):
        print 'Starting publisher'
        self.serverThread     = threading.Thread()
        self.serverThread.run = self.run_server
        self.serverThread.setDaemon( True )
        self.serverThread.start()
        print 'Thread started'
    
    def publish( self ):
        # Trigger the publisher to send a frame of data
        if self.conn != None and len(self.subscriptions):
            try:
                frame = {k:self.catalog[k]() for k in self.subscriptions}
                self.conn.send(pickle.dumps(frame))
            except error, mesg:
                print mesg
                self.restart()

    def restart( self ):
        self.subscriptions = []
        self.restartflag = 1
        self.conn.close()
        self.conn = None
        self.serverThread.join()
        self.restartflag = 0
        self.start()

    def run_server( self ):
        print 'Hello from the server thread'
        self.sock = socket( AF_INET, SOCK_STREAM )
        addr = ('localhost', self.port)
        # This is a hack to allow fast restarts
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind( (addr) )
        self.sock.listen(1)
        self.conn,self.remote_addr = self.sock.accept()
        # Send a copy of the catalog
        s = pickle.dumps(self.catalog.keys())
        self.conn.send(s)
        print 'Entering server loop'
        # Main server loop
        while not self.restartflag:
            # Wait for request
            try:
                s = self.conn.recv(4096)
            except error, mesg:
                print mesg
                self.restartflag = 1
            if s:
                # The request must be a list of catalog keys
                try:
                    keys = pickle.loads(s)
                    print "Received subscription list:"
                    print keys
                    self.subscriptions = keys
                except:
                    print 'Pickle fail'
            else:
                print "Timed out without receiving"
        self.sock.close()

    def close( self ):
        print 'Closing publisher gracefully'
        self.conn.close()
        self.sock.close()

class Subscriber:
    def __init__(self, host, port):
        # Connect to the target publisher
        self.frameReceivedCallback = None
        self.clientThread = None
        self.sock = socket( AF_INET, SOCK_STREAM )
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        while 1:
            try:
                self.sock.connect( (host,port) )
                self.catalog = pickle.loads(self.sock.recv(4096))
                break
            except error, desc:
                print desc
                time.sleep(1.0)
        print 'Received catalog!'
        self.catalog.sort()
        print self.catalog
    def start( self ):
        self.clientThread = threading.Thread()
        self.clientThread.run = self.run_client
        self.clientThread.setDaemon( True )
        self.clientThread.start()
    def subscribeTo( self, name_list ):
        self.sock.send( pickle.dumps(name_list) )
    def run_client( self ):
        # The client waits to receive frames and then calls the callback
        while 1:
            try:
                frame = pickle.loads(self.sock.recv(4096))
                self.frameReceivedCallback( frame )
            except error, mesg:
                # Socket error
                print mesg
            except:
                'What just happened?'
    def setCallback( self, callback ):
        self.frameReceivedCallback = callback
    def close( self ):
        print 'Closing subscriber gracefully'
        self.sock.close()

def dummy_callback( frame ):
    print 'Got frame!'
    for k,v in frame.items():
        print k,v

if __name__=='__main__':
    p = Publisher(5056)
    import random
    p.addToCatalog('mydick', lambda: random.uniform(0,1))
    p.addToCatalog('ass', lambda: random.uniform(0,1))
    p.start()
    time.sleep(0.1)
    s = Subscriber( 'localhost', 5056 )
    s.setCallback( dummy_callback )
    s.subscribeTo(['mydick'])
    s.start()
    for x in range(100):
        p.publish()
        time.sleep(0.01)
    p.close()
    s.close()
    time.sleep(0.1)
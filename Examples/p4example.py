from P4 import P4, P4Exception    # Import the module

p4 = P4()                        # Create the P4 instance
p4.port = 'localhost:1666'
p4.user = 'fred'
p4.client = 'fred-ws'            # Set some environment variables

try:                             # Catch exceptions with try/except
    p4.connect()                   # Connect to the Perforce Server
    info = p4.run('info')          # Run "p4 info" (returns a dict)
    for key in info[1]:            # and display all key-value pairs
        print '%s = %s' % (key, info[1][key])
    p4.disconnect()                # Disconnect from the Server
except P4Exception:
    for e in p4.errors:            # Display errors
        print e
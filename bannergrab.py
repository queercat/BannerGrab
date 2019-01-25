import argparse # Parsing arguments.
import socket # Connecting to things.
import time # Creating logs and sleeping threads. 

# get_args ... getsCLI arguments using argparser.
def get_args():
    parser = argparse.ArgumentParser(description='Grab SSH, FTP, and HTTP banners.')
    parser.add_argument('hosts', type=str, help='CSV list of addresses to grab from.') 
    parser.add_argument('-p', '--ports', type=str, default='22,25,80', help='CSV list of ports {default: %(default)s}')
    parser.add_argument('-n', '--no-log', action='store_true', help='no log file')
    parser.add_argument('-t', '--timeout', type=int, nargs=1, default=5, help='time (in seconds) to wait before closing connection {default: %(default)s}')
    parser.add_argument('-v', '--verbose', action='store_true', help='verboes  printing')
    return parser.parse_args()

def main():
    a = get_args() # Get the CLI args.
    grab(a.hosts, a.ports, not a.no_log, a.timeout, a.verbose)

def grab(hosts, ports, logging, timeout, verbose):
    # GET HOST:
    # CONNECT -> LISTEN [TIMEOUT] -> ?LOG PRINT [loop]

    logo = '''
__________                                     ________            ___.                      
\______   \____    ____   ____   ___________  /  _____/___________ \_ |__      ______ ___.__.
 |    |  _|__  \  /    \ /    \_/ __ \_  __ \/   \  __\_  __ \__  \ | __ \     \____ <   |  |
 |    |   \/ __ \|   |  \   |  \  ___/|  | \/\    \_\  \  | \// __ \| \_\ \    |  |_> >___  |
 |______  (____  /___|  /___|  /\___  >__|    \______  /__|  (____  /___  / /\ |   __// ____|
        \/     \/     \/     \/     \/               \/           \/    \/  \/ |__|   \/     
'''

    print(logo)

    hosts = hosts.split(',')
    ports = ports.split(',')


    # Write in custom behaviors here.
    port_req = {
        22: ['\r\n\r\n'],
        25: ['\r\n\r\n'],
        80: ['HEAD / HTTP/1.0\r\n\r\n', 'HEAD / HTTP/1.1\r\nHost: host:port\r\n\r\n', '']  
    }

    log = []

    for host in hosts:
        address_down = True # We assume it is to start out. 

        for port in ports:
            sock = socket.socket()
            sock.settimeout(int(timeout))

            port = int(port)

            connect = '*'
            greeting = '*'
            msgs = []
            msg = '*'
            resps = []
            resp = '*'

            try:
                sock.connect((host, port))

            except socket.timeout:
                if address_down:  
                    connect = 'Address down or address\' port closed.'
                else:
                    connect = 'Port closed.'

            except Exception as e:
                connect = str(e)
                address_down = True

            else:
                connect = 'Connection successful.'
                address_down = False

            if not address_down:
                try:
                    greeting = recv(sock, 4096)
                except socket.timeout:
                    greeting = 'empty greeting'

                for msg in port_req.get(port, ''):
                    try:
                        msgs.append(msg)
                        send(sock, msg)

                        resp = recv(sock, 4096)

                        if resp is '':
                            resp = 'empty response'
                    except socket.timeout: 
                        resp = 'empty response'
                    
                    else:
                        resps.append(resp)

            full_data = [host, port, connect, greeting, msgs, resps]
            full_data_desc = ['host', 'port', 'connection', 'greeting', 'messages', 'responses']

            if verbose:
                pretty_print(full_data, full_data_desc)
            
            log.append(full_data)

            sock.close()

# pretty_print ... Prints data all pretty.
def pretty_print(data, data_desc):
    for val in range(0, len(data)):
        if type(data[val]) is not list:
            print(str(data_desc[val]) + ': ' + str(data[val]).rstrip('\n'))
        else:
            print('--------------------------------')
            max_length = get_max(data[val])

            for element in range(0, len(data[val])):
                # num_of_spaces = (max_length - len(data[val][element])) + 1
                # spaces = ' ' * num_of_spaces
                print(data[val][element] + ' [' + str(element) + ']')
    
    print('--------------------------------')
    print('\n')

# get_max ... Returns the max number of characters in a list of strings.
def get_max(lizt):
    max = -1

    for element in lizt:
        length = len(element)
        
        if length > max:
            max = length
        
    return max

# recv ... A cleaner way of recieving data.
def recv(sock, bufsize):
    data = ''

    while True:
        buffer = sock.recv(bufsize)
        data += buffer.decode('utf-8')

        if not buffer:
            break

    return data

# send ... A clean way of sending data.
def send(sock, msg):
    sock.send(msg.encode())

if __name__ == "__main__":
    main()

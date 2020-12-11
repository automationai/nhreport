#!/usr/bin/env python3
import sys
import getopt
import socket

def check_port(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((ip,port))
    if result == 0:
        status = 'open'
    else:
        status = 'close'
    print('Port {} status on host {} is: {}'.format(port,ip,status))
    s.close()

def main(argv):
    ip = ''
    port = 0
    fn = ''
    try:
        opts, args = getopt.getopt(argv,'hi:p:f:',['ip=','port=','file='])
        #print(args)
    except getopt.GetoptError:
        print('Usage: port_test.py -i <ip> -p <port> || port_test.py -f <file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: port_test.py -i <ip> -p <port> || port_test.py -f <file>')
            sys.exit()
        elif opt in ('-i','--ip'):
            ip = arg
        elif opt in ('-p','--port'):
            port = int(arg)
        elif opt in ('-f','--file'):
            fn = arg
    if len(fn) != 0:
        print('--file option detected, ignore --ip & --port options...')
        with open(fn) as fh:
            for line in fh:
                ip = line.rstrip().split(" ")[0]
                port = int(line.rstrip().split(" ")[1])
                check_port(ip,port)
        return
    if ip !='' and port !=0:
        check_port(ip,port)
    else:
        print('Missing options!\nUsage: port_test.py -i <ip> -p <port> || port_test.py -f <file>')
        

if __name__ == "__main__":
    print('Network Port Test Tool 1.0! Author: Jason.Pan@Aveva.com\nhttps://github.com/junclimber/utilities')
    main(sys.argv[1:])
    print('The End')

#!/usr/bin/env python3
import sys
import getopt
import socket
import emails

def check_port(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((ip,port))
    if result == 0:
        status = 'open'
    else:
        status = 'close'
    s.close()
    return 'Port {} status on host {} is: {}'.format(port,ip,status)

def main(argv):
    ip = ''
    port = 0
    fn = ''
    result = ''
    sender = ''
    recipient = ''
    host = ''
    help = 'Usage:\n  port_test.py -i <ip> -p <port> [-r <recipient> -s <sender> -t <host>]\n  port_test.py -f <file> [-r <recipient> -s <sender> -t <host>]'
    try:
        opts, args = getopt.getopt(argv,'hi:p:f:r:s:t:',['ip=','port=','file=','recipient=','sender=','host='])
        #print(args)
    except getopt.GetoptError:
        print(help)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help)
            sys.exit()
        elif opt in ('-i','--ip'):
            ip = arg
        elif opt in ('-p','--port'):
            port = int(arg)
        elif opt in ('-f','--file'):
            fn = arg
        elif opt in ('-r','--recipient'):
            recipient = arg
        elif opt in ('-s','--sender'):
            sender = arg
        elif opt in ('-t','--host'):
            host = arg

    if fn == '':
        if ip !='' and port !=0:
            result = check_port(ip,port)
        else:
            print('Missing options!\n'+help)
    else:
        if ip !='' or port !=0:
            print('Cannot have both -i-p and -f\n'+help)
        else:
            with open(fn) as fh:
                for line in fh:
                    ip = line.rstrip().split(" ")[0]
                    port = int(line.rstrip().split(" ")[1])
                    result += '\n' + check_port(ip,port)

    print(result.strip()+'\n')
    if len(recipient) != 0 and len(sender) != 0 and len(host) != 0:
        subject = "Ports status report"
        message = emails.generate_email(sender,recipient,subject,result)
        emails.send_email(message,host)
        print('Notification message sent to {}'.format(recipient))
    elif len(recipient) == 0 and len(sender) == 0 and len(host) == 0:
        print('Notification options didn\'t set, no messages sent')
    else:
        print('Missing options! Recipent, sender & mail host are all required arguments to send notifications!')

if __name__ == "__main__":
    print('Network Port Test Tool 1.0! Author: Jason.Pan@Aveva.com\nhttps://github.com/junclimber/utilities\n')
    main(sys.argv[1:])
    print('\n')

#!/usr/bin/env python3
import sys
import getopt
import socket
import emails

def portstatus(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((ip,port))
    if result == 0:
        status = 'open'
    else:
        status = 'close'
    s.close()
    return status

def main(argv):
    ip = ''
    port = 0
    fn = ''
    result = ''
    sender = ''
    recipient = ''
    subject = "Network Health Report"
    body = "Here's your Calgary R&D Lab network services health report:\n"
    host = ''
    help = 'Usage:\n  port_test.py -i <ip> -p <port> [-r <recipient> -s <sender> -t <host>]\n  port_test.py -f <file> [-r <recipient> -s <sender> -t <host>]'
    try:
        opts, _ = getopt.getopt(argv,'hi:p:f:r:s:t:',['ip=','port=','file=','recipient=','sender=','host='])
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
            result = 'Port {} status on host {} is: {}'.format(port,ip,portstatus(ip,port))
            print(result)
            body += '\n{}'.format(result)
        else:
            print('Missing options!\n'+help)
    else:
        if ip !='' or port !=0:
            print('Cannot have both -i-p and -f\n'+help)
        else:
            try:
                with open(fn) as fh:
                    for line in fh:
                        ip = line.rstrip().split(" ")[0]
                        port = int(line.rstrip().split(" ")[1])
                        result = 'Port {} status on host {} is: {}'.format(port,ip,portstatus(ip,port))
                        print(result)
                        body += '\n{}'.format(result)
            except IOError as e:
                print(e)

    if len(recipient) != 0 and len(sender) != 0 and len(host) != 0:
        message = emails.generate_email(sender,recipient,subject,body)
        send_status = emails.send_email(message,host)
        if send_status == 1:
            print('\nNotification message sent to {}'.format(recipient))
    elif len(recipient) == 0 and len(sender) == 0 and len(host) == 0:
        print('\nNotification options didn\'t set, no messages sent')
    else:
        print('Missing options! Recipent, sender & mail host are all required arguments to send notifications!')

if __name__ == "__main__":
    print('Network Services Health Report Tool 0.1 - Author: Jason.Pan@Aveva.com\nhttps://github.com/automationai/nshreport\n')
    main(sys.argv[1:])
    print('\n')

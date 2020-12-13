#!/usr/bin/env python3
import argparse
import configparser
import socket
import emails
import re
import sys
import os

def portstatus(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((ip,port))
    if result == 0:
        status = 'open'
    else:
        status = 'close'
    s.close()
    return status

def main():
    body = 'Network Services Health Report Tool 0.1 - Author: Jason.Pan@Aveva.com\n'
    body += 'https://github.com/automationai/nshreport\n\n'
    body += "Here's your network services health report:"

    parser = argparse.ArgumentParser()
    group1 = parser.add_mutually_exclusive_group(required=True)
    group1.add_argument('-a','--address',help='IP address with port, format <ip>:<port>')
    group1.add_argument('-f','--file',help="File name with addresses list, format for each line in file: <ip> <port>")
    group2 = parser.add_argument_group('Notification arguments')
    group2.add_argument('-n','--notification',action='store_true',help="Enable email notification")
    group2.add_argument('-r','--recipient',help='Notification email recipient')
    group2.add_argument('-s','--sender',help='Notification email sender')
    group2.add_argument('-m','--smtp_server',help='SMTP server IP address')
    args = parser.parse_args()

    print(body)

    if args.address is not None:
        if re.search(r'^[\w.]+:\d+$',args.address):
            ip = args.address.split(':')[0]
            port = int(args.address.split(':')[1])
            result = '- Port {} status on host {} is: {}'.format(port,ip,portstatus(ip,port))
            print(result)
            body += '\n{}'.format(result)
        else:
            print('Wrong address format! it should be <ip>:<port>')
    else:
        try:
            with open(args.file) as fh:
                n = 0
                for line in fh:
                    n += 1
                    if re.search(r'^[\w.]+ \d+$',line):
                        ip = line.rstrip().split(" ")[0]
                        port = int(line.rstrip().split(" ")[1])
                        result = '- Port {} status on host {} is: {}'.format(port,ip,portstatus(ip,port))
                        print(result)
                        body += '\n{}'.format(result)
                    else:
                        print('Wrong address format in line {}: {}! it should be <ip> <port>'.format(n,line.rstrip()))
                    
        except IOError as e:
            print('\n{}'.format(e))
            sys.exit()

    if args.notification:
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.expanduser('~'),'nshreport.ini'))
        try:
            company = config['DEFAULT']['company'].strip()
            recipient = config['DEFAULT']['recipient'].strip()
            sender = config['DEFAULT']['sender'].strip()
            smtp_server = config['DEFAULT']['smtp_server'].strip()
        except KeyError:
            print('\nPlease create or copy nshreport.ini in you home folder before sending notification!\nRefer https://github.com/automationai/nshreport/blob/main/README.md')
            sys.exit()
        subject = "{} Network Service Health Report".format(company)
        body += "\n\nReport provided by {} IT Automation Team".format(company)

        print('\n')
        if args.recipient is not None:
            recipient = args.recipient
        elif recipient != '':
            print('-> recipient not specified, use default: {}'.format(recipient))
        else:
            print('-> No recipient configured, please specify it with -r or add it in nshreport.ini file! no message will be sent!')
            return

        if args.sender is not None:
            sender = args.sender
        elif sender != '':
            print('-> sender not specified, use default: {}'.format(sender))
        else:
            print('-> No sender configured, please specify it with -s or add it in nshreport.ini file! no message will be sent!')
            return

        if args.smtp_server is not None:
            smtp_server = args.smtp_server
        elif smtp_server != '':
            print('-> smtp server not specified, use default: {}'.format(smtp_server))
        else:
            print('->No smtp server configured, please specify it with -m or add it in nshreport.ini file! no message will be sent!')
            return

        message = emails.generate_email(sender,recipient,subject,body)
        send_status = emails.send_email(message,smtp_server)
        if send_status:
            print('\nNotification message sent to {}'.format(recipient))
        else:
            print('\nCould not connect to smtp server! no messages sent!')
    else:
        print('\nNotification arguments isn\'t enabled, no messages will be sent')
        
if __name__ == "__main__":
    main()
    print('\n')

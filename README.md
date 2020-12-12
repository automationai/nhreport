# utilities

## Port Test Tool
### Usage:
#### Test single IP & Port:
`port_test.py -i <ip> -p <port>`
#### Test IP & Port loaded from a file:
`port_test.py -f <file>`
##### File format: `<ip> <port>` without header. e.g.
```
191.168.0.3 80
192.168.0.10 3389
192.168.2.5 445
```

## To do list
- change names: jason / automation / nhreport (Network Health Report)
- handle exceptions
- check_port -> port_status, simplify return value
- print on screen result line by line
- cron
- try windows python result
- compile windows exe
- update documents, detail help file

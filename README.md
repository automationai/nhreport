# Network Service Health Report Tool
Current Version: 0.1
## Use Cases
- Scheduled network service health report - with cron or Windows Task Scheduler
- Network service port testing after major changes

## Sample Email Report
![sample](sample.png)

## Download
### Windows
### Debian
### Mac

## Configuration file
- .nshconfig file is required if you enable -n to send notifications
- The file will be generate first time you run the tool and be placed at your home folder

Sample configuration file:

![ini](ini.png)

## Usage
### Get help
`nshreport -h`
![help](help.png)
### Test single IP & Port
`nshreport -a <ip>:<port>`
### Test IP & Port loaded from a file
`nshreport -f <file>`
### Test IP & Port loaded from a file and send email notification with config file
`nshreport -f <file> -n`
### Test IP & Port loaded from a file and send email notification with command line
`nshreport -f <file> -n -r <recipient> -s <sender> -m <smtp_server>`

## Source address file
Format each line as <ip> <port>

![source](source.png)

## Result
![result](result.png)

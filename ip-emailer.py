import json
from subprocess import Popen, PIPE
import smtplib
from socket import gaierror
import string
import os

with open('email_info.json') as f:
    EMAIL = json.load(f)
print(EMAIL['USER'], EMAIL['PASS'])


SENDER = {}
RECEIVER = {}

SENDER['addr'] = EMAIL['USER']
SENDER['pass'] = EMAIL['PASS']
SENDER['serv'] = 'smtp.gmail.com'
SENDER['port'] = 465  # default GMAIL SMTP port
RECEIVER['addr'] = EMAIL["RECEIVER"]; 
# Note: RECEIVER['addr']  must be a list (ie don't delete the brackets)!
# This allows the specification of a list of addresses ['me@addr.com', 'you@addr.com', 'them@addr.com']
# specify the interface to query
INTERFACE = 'en0' # default interface for a Raspberry Pi
HOSTNAME_raw = Popen('hostname', stdout=PIPE)
HOSTNAME = HOSTNAME_raw.communicate()[0].decode('utf-8').replace('\n','')

p1 = Popen(['curl', 'https://checkip.amazonaws.com'], stdout=PIPE)
the_ip = p1.communicate()[0].decode('utf-8').replace('\n','')
print('found {} as the ip'.format(the_ip))

if not os.path.exists('old_ip'):
    print('no path, creating one now')
    with open('old_ip', 'w') as f:
        f.write(the_ip)
        f.write('\n')
    exit()
else:
    with open('old_ip', 'r') as f:
        old_ip = f.read().split('\n')[0]
    if old_ip == '':
        print("file emtpy")
        print("found old_ip file but it is empty, re-writing now")
        with open('old_ip','w') as f:
            f.write(the_ip)
        exit()

if old_ip == the_ip:
    print('ip did not change')
    exit()


TO = RECEIVER['addr']
FROM = SENDER['addr'] 
BODY = the_ip

SUBJECT = "{}'s IP on {}".format(HOSTNAME, INTERFACE)
BODY = "Subject: {}\n\n{}".format(SUBJECT, BODY)

# Try to send the email
try:
	server = smtplib.SMTP_SSL( SENDER['serv'], SENDER['port'] )     # NOTE:  This is the GMAIL SSL port.
	server.login( SENDER['addr'], SENDER['pass'] )
	server.sendmail( FROM, TO, BODY )
	server.quit()
	print('sent email. exiting.')

except smtplib.SMTPAuthenticationError:
	print("Error, authentication failed! Please check your username and password.")

except gaierror:
	print('Error, cannot connect to: {}!  Please ensure it is a valid smtp server.'.format(SENDER['serv']))
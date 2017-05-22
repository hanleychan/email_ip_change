"""
Sends an email whenever the external IP address is changed.
"""

import requests, json, smtplib

receiver_email = ''
sender_email = ''
sender_password = ''
smtp_server = 'smtp.gmail.com'
smtp_port = 587

def send_email(email_subject, email_body):
    global receiver_email, sender_email, sender_password, smtp_server, smtp_port

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(sender_email, sender_password)

    message = 'Subject: {}\n\n{}'.format(email_subject, email_body)

    try:
        server.sendmail(sender_email, receiver_email, message) 
    except:
        pass
    
    server.quit()

if __name__ == '__main__':
    data_filename = 'ip_info.txt'

    try:
        data_file = open(data_filename, 'r+')
        prev_ip = json.loads(data_file.read())['ip']
    except FileNotFoundError:
        data_file = open(data_filename, 'w')
        prev_ip = None

    json_data = requests.get('http://ipinfo.io/json').json()
    external_ip = json_data['ip']

    if prev_ip != external_ip or not prev_ip :
        data_file.truncate()
        data_file.write(json.dumps(json_data));

        email_subject = 'IP Address Change Notification'
        email_body = f'New IP Address: {external_ip}\n'
        email_body += f'Previous IP Address: {prev_ip}\n'

        send_email(email_subject, email_body)
        
    data_file.close()

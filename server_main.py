
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import smtplib
from datetime import datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import xml.etree.ElementTree as Et
import sys

import paramiko

import models
import settings


def main():
    tree = Et.parse(settings.CONFIG_FILE_PATH)
    data = tree.getroot()
    for client in data:
        get_stats(client)
    return data


def get_stats(client):
    client_data = client.attrib
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())
    ssh.connect(client_data['ip'], username=client_data['username'], password=client_data['password'], port=int(client_data['port']))
    sftp = ssh.open_sftp()
    sftp.put('client_main.py', '/tmp/client_main.py')
    sftp.put('requirements.txt', '/tmp/requirements.txt')
    stdin, stdout, stderr = ssh.exec_command("sudo pip install -r /tmp/requirements.txt", get_pty=True)
    stdin.write(client_data['password'] + "\n")
    stdin.flush()
    print stderr.read()
    print stdout.read()
    stdin, stdout, stderr = ssh.exec_command("python /tmp/client_main.py")
    stats = stdout.read()
    stats = json.loads(stats)
    add_stats(client_data, stats)
    send_alert(client, stats)
    print stderr.read()
    return stats


def add_stats(client_data, stats):
    stats[u'ip'] = client_data['ip'].decode("utf-8")
    engine = create_engine('sqlite:///client_statistics.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    machine_stat = models.add(stats)
    print stats
    print machine_stat.ip
    session.add(machine_stat)
    session.commit()


def send_alert(client, stats):
    for alert in client.findall('alert'):
        alert_data = alert.attrib
        if int(alert_data['limit'][:-1]) <= int(stats[(alert_data['type'] + "_usage")]):
            try:
                sender = settings.SENDER
                message = MIMEMultipart()
                message['From'] = sender
                message['To'] = client.attrib['mail']
                message['subject'] = "%s usage limit exceeded" % alert_data['type']
                body = """
                 Dear Admin
                    You have exceeded usage limit exceeded. Please look into it  ASAP.

                Thanks
                """
                message.attach(MIMEText(body, 'plain'))
                message = message.as_string()
                smtp_client = smtplib.SMTP(settings.SMTP_HOST)
                smtp_client.sendmail(sender, client.attrib['mail'], message)
                print "Alert sent"
            except smtplib.SMTPException:
                print "Error: unable to send email"


if __name__ == '__main__':
    main()

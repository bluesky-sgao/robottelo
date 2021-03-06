"""
Utility module to handle the shared ssh connection
"""

import logging
import re
import socket
import sys
import time

from robottelo.common import conf
from robottelo.common.constants import SSH_CHANNEL_READY_TIMEOUT
from robottelo.common.helpers import csv_to_dictionary
from robottelo.common.helpers import sleep_for_seconds
from select import select

try:
    import paramiko
except ImportError:
    print "Please install paramiko."
    sys.exit(-1)


class CommandTimeOut(Exception):
    """
    Exception for Paramiko timeouts
    """
    pass


class SSHCommandResult(object):
    """
    Structure that returns in all ssh commands results.
    """

    def __init__(self, stdout=None, stderr=None,
                 return_code=0, transform_csv=False):
        self.stdout = stdout
        self.stderr = stderr
        self.return_code = return_code
        self.transform_csv = transform_csv
        #  Does not make sense to return suspicious CSV if ($? <> 0)
        if transform_csv and self.return_code == 0:
            self.stdout = csv_to_dictionary(stdout) if stdout else {}


def _get_connection(timeout=10):
    """
    Constructs a ssh connection to the host provided in config.
    """
    # Hide base logger from paramiko
    logging.getLogger("paramiko").setLevel(logging.ERROR)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    host = conf.properties['main.server.hostname']
    root = conf.properties['main.server.ssh.username']
    key_filename = conf.properties['main.server.ssh.key_private']
    client.connect(
        host, username=root, key_filename=key_filename, timeout=timeout)
    logging.getLogger('robottelo').info(
        "Paramiko instance prepared (and would be reused): %s"
        % hex(id(client))
    )
    return client


# Define the shared ssh connection
connection = _get_connection()


def upload_file(local_file, remote_file=None):
    """
    Uploads a remote file to a normal server or
    uploads a file to sauce labs via VPN tunnel.
    """

    remote = int(conf.properties['main.remote'])

    if not remote_file:
        remote_file = local_file

    if not remote:
        sftp = connection.open_sftp()
        sftp.put(local_file, remote_file)
        sftp.close()
    # TODO: Upload file to sauce labs via VPN tunnel in the else part.


def command(cmd, hostname=None, expect_csv=False, timeout=None):
    """
    Executes SSH command(s) on remote hostname.
    Defaults to main.server.hostname.
    """

    # Set a default timeout of 60 seconds
    if timeout is None:
        timeout = 60

    # Start the timer
    start = time.time()
    # Variable to hold results returned from the command
    stdout = stderr = errorcode = None

    # Remove escape code for colors displayed in the output
    regex = re.compile(r'\x1b\[\d\d?m')

    logger = logging.getLogger('robottelo')
    logger.debug(">>> %s" % cmd)

    hostname = hostname or conf.properties['main.server.hostname']

    channel = connection.get_transport().open_session()
    channel.settimeout(timeout)
    channel.exec_command(cmd)

    sleep_counter = 0
    while True:
        try:
            rlist, wlist, elist = select([channel], [], [], float(timeout))
            while (not channel.recv_ready() and
                   not channel.recv_stderr_ready() and
                   sleep_counter < SSH_CHANNEL_READY_TIMEOUT * 10):
                        sleep_for_seconds(0.1)
                        sleep_counter += 1
            if rlist is not None and len(rlist) > 0:
                if channel.exit_status_ready():
                    stdout = channel.recv(1048576)
                    stderr = channel.recv_stderr(1048576)
                    errorcode = channel.recv_exit_status()
                    break
            elif elist is not None and len(elist) > 0:
                if channel.recv_stderr_ready():
                    stdout = channel.recv(1048576)
                    stderr = channel.recv_stderr(1048576)
                    break

            if time.time() - start > timeout:
                logger.debug("Command timeout exceeded.")
                raise CommandTimeOut('Command timeout exceeded')
        except socket.timeout:
            logger.debug("SSH channel timeout exceeded.")
            raise CommandTimeOut('SSH channel timeout exceeded.')

    # For output we don't really want to see all of Rails traffic
    # information, so strip it out.

    if stdout:
        # Empty fields are returned as "" which gives us u'""'
        stdout = stdout.replace('""', '')
        stdout = stdout.decode('utf-8')
        stdout = u"".join(stdout).split("\n")
        output = [
            regex.sub('', line) for line in stdout if not line.startswith("[")
            ]
    else:
        output = []

    # Ignore stderr if errorcode == 0. This is necessary since
    # we're running Foreman in verbose mode which generates a lot
    # of output return as stderr.
    errors = [] if errorcode == 0 else stderr

    if output:
        logger.debug("<<<\n%s" % '\n'.join(output[:-1]))
    if errors:
        errors = regex.sub('', "".join(errors))
        logger.debug("<<< %s" % errors)

    return SSHCommandResult(
        output, errors, errorcode, expect_csv)

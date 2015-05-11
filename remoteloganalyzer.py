__author__ = 'Avinesh_Kumar'

import paramiko
import argparse
import logging
import sys
import os
import time
import loganalyzer
import properties


LOCALMODE = 'local'
REMOTEMODE = 'remote'

parser = argparse.ArgumentParser(description="remote log analyzer.")
subparsers = parser.add_subparsers(dest='loganalyzer', help='remote log analyzer.')
localparser = subparsers.add_parser('local')
localparser.add_argument("-c", "--config", help="Name of config file, optional argument, "
                                                "default value = analyzer.properties",
                         default="analyzer.properties")
localparser.add_argument("-r", "--report", help="name of report, optional argument, "
                                                "default value = loganalyzerReport.txt",
                         default="loganalyzerReport.txt")

remoteparser = subparsers.add_parser('remote')
remoteparser.add_argument("-i", "--host", required=True, help="ip of remote host")
remoteparser.add_argument("-u", "--username", required=True, help="username of remote host")
remoteparser.add_argument("-p", "--password", required=True, help="password of remote host")
remoteparser.add_argument("-c", "--config", help="Name of config file, optional argument, "
                                                 "default value = analyzer.properties",
                          default="analyzer.properties")
remoteparser.add_argument("-d", "--reportdir", help="path of report directory, optional argument, "
                                "default value = .",
                          default=".")
remoteparser.add_argument("-r", "--report", help="name of report, optional argument, "
                                                 "default value = loganalyzerReport.txt",
                          default="loganalyzerReport.txt")

args = parser.parse_args()

mode = args.loganalyzer

logfile_dir = ""
logfile = ""

server = ""
username = ""
password = ""
reports_dir = os.getcwd()
reportName = args.report
configfileName = args.config


if mode == REMOTEMODE:
    server = args.host
    username = args.username
    password = args.password
    reports_dir = args.reportdir


analyzer_remote_home = "/tmp/LogAnalyzer"
analyzer_remote_report_home = properties.loadproperties(configfileName).get('output.file.dir')

logger_name = sys.argv[0].split('.')
logger = logging.getLogger(logger_name[0])
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


logger.info("server ip: " + server)
logger.info("username: " + username)
logger.info("password: " + password)
logger.info("report Name: " + reportName)
logger.info("report dir: " + reports_dir)
# sys.exit(0)

files_tcp = ['loganalyzer.py', 'fileutil.py', 'properties.py']
files_cp_remote = list()
for ftc in files_tcp:
    files_cp_remote.append(ftc)
files_cp_remote.append(configfileName)


def copyfiletoremote(sshconn, files, dst):
    sftp = sshconn.open_sftp()
    for f in files:
        sftp.put(f, dst + "/" + f)
    sftp.close()


def copyfilefromremote(sshconn, files, dst):
    sftp = sshconn.open_sftp()
    for f in files:
        sftp.put(f, dst + "/" + f)
    sftp.close()


def runlocally(logfiledir, logfilename, report):
    if os.path.exists(logfilename):
        bkpfile = logfilename + ".bkp_" + str(int(time.time()))
        logger.info(logfilename + " already exists. Taking backup of the file to " + bkpfile)
        os.rename(logfilename, bkpfile)

    logger.info("Analyzing logs...")
    loganalyzer.analyze(configfileName, report, None)
    logger.info("DONE")


def runonwindowsserver(files_to_copy, analyzer_root, analyzer_reports_root, reportdir, report):
    pass


def runonlinuxserver(ssh, files_to_copy, analyzer_root, analyzer_reports_root, reportdir, report):
    """

    :type report:
    """
    mkstdin, mkstdout, mkstderr = ssh.exec_command('mkdir -p ' + analyzer_root)
    mkdir_err = mkstderr.readlines()
    if mkdir_err:
        logger.error(mkdir_err)

    logger.info("copying the files to remote server.")
    copyfiletoremote(ssh, files_to_copy, analyzer_root)
    logger.info("finished copying the files to remote server.")

    chstdin, chstdout, chstderr = ssh.exec_command('chmod 777 ' + analyzer_root + '/loganalyzer.py')
    chmod_out = chstdout.readlines()
    chmod_err = chstderr.readlines()
    if chmod_err:
        logger.error(chmod_err)

    logger.info("Analyzing logs...")
    logger.info("It may take few minutes, depends on number of files and size of the files.")
    stdin, stdout, stderr = ssh.exec_command(
        'python ' + analyzer_root + '/loganalyzer.py ' + configfileName + ' ' + report)
    analyzer_out = stdout.readlines()
    analyzer_err = stderr.readlines()
    if not analyzer_err:
        logger.info(analyzer_out)
    else:
        logger.error(analyzer_err)

    catstdin, catstdout, catstderr = ssh.exec_command('cat ' + analyzer_reports_root + '/' + report)
    # print catstdout.readlines()
    if os.path.exists(os.path.join(reportdir, report)):
        bkpfile = report + ".bkp_" + str(int(time.time()))
        logger.info(report + " already exists. Taking backup of the file to " + bkpfile)
        os.rename(os.path.join(reportdir, report), os.path.join(reportdir, bkpfile))

    with open(os.path.join(reportdir, report), 'w') as reportfile:
        logger.info("generating report...")
        reportfile.writelines(catstdout.readlines())
        reportfile.writelines(catstderr.readlines())
        reportfile.flush()
        logger.info(
            "Report is generated. Please check the report here: " + os.path.join(reportdir, report))


def runremotely(ssh, files_to_copy, analyzer_root, analyzer_reports_root, reportdir, report, ostyp):
        """

        :rtype : object
        """
        if ostyp == 0:
            runonwindowsserver(files_to_copy, analyzer_root, analyzer_reports_root, reportdir, report)
        elif ostyp == 1:
            runonlinuxserver(ssh, files_to_copy, analyzer_root, analyzer_reports_root, reportdir, report)


def connect(host, user, passwd):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        logger.info("connecting to the server " + server)
        ssh.connect(server, username=username, password=password)
        logger.info("connected")
        return ssh


def main():
        if mode == LOCALMODE:
            runlocally(logfile_dir, logfile, reportName)
        elif mode == REMOTEMODE:
            sshconn = connect(server, username, password)
            runremotely(sshconn, files_cp_remote, analyzer_remote_home, analyzer_remote_report_home, reports_dir,
                        reportName, ostyp=1)
            sshconn.close()


if __name__ == "__main__":
        main()



__author__ = 'Avinesh_Kumar'

import os
import time
import logging
import properties
import fileutil
import glob
import sys

# logger_name = sys.argv[0].split('.')
logger = logging.getLogger("loganalyzer")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def getlogfiles(hr, minutes, logfilefilter):
    if not hr:
        past = time.time() - float(minutes) * 60  # 2 hours
    else:
        past = time.time() - float(hr) * 60 * 60
    list_of_log_files = []

    files = glob.glob(logfilefilter)

    if int(hr) or int(minutes):
        for fl in files:
            if os.path.getmtime(fl) >= past:
                list_of_log_files.append(fl)
    else:
        list_of_log_files = files

    return list_of_log_files


def analyze(configfileName, reportname, logfile=None):
    propertiesfilepath = os.path.dirname(os.path.abspath(__file__))+os.path.sep+configfileName
    default_regex = ['(?:.*\W)?(.*Exception)']

    # (?:.*ERROR) '(^ERROR)', (?!.*(INFO|DEBUG))(?:(?!.*class\.method).*(?:\.|\=))(.*Exception)
    # ['(^ERROR)', '^(?!INFO|DEBUG)(?:(?!.*class\.method).*\W*)(^.*Exception)(?:.*)']

    props = properties.loadproperties(propertiesfilepath)
    dirpath = props.get('log.file.dir')
    keywordsSep = props.get('search.keywords.seperator')
    keywords = props.get('search.keywords')
    defaultsearch = int(props.get('disable.default.search'))
    limit = int(props.get('pre.post.line.limit'))

    # initializing list of keywords to search in line
    list_of_keywords = keywords.split(keywordsSep)
    # assert isinstance(defaultsearch, object)
    if (len(list_of_keywords) == 1) and not list_of_keywords[0]:
        list_of_keywords.pop()
        if not defaultsearch:
            for k in default_regex:
                list_of_keywords.append(k)
        elif not defaultsearch:
            for k in default_regex:
                list_of_keywords.append(k)

    reportfilepath = props.get('output.file.dir') + os.path.sep + reportname
    # "output-report" + str(int(time.time())) + ".txt"
    logfilepat = props.get('log.file.pattern')
    logfilefilter = dirpath + os.path.sep + logfilepat

    excludes = props.get('exclude.keyword.list').split(keywordsSep)
    hr = props.get('time.in.hr')
    minutes = props.get('time.in.min')

    logger.info('log base dir: %s', dirpath)
    logger.info('time in hr: %s', hr)
    logger.info('time in min: %s', minutes)
    logger.info("file pattern: %s", logfilefilter)
    logger.info("exclude list: %s", excludes)
    # logging.info("files: %s",glob.glob(logfilefilter))
    past = time.time()

    list_of_log_files = []

    if logfile:
        list_of_log_files.append(logfile)
    else:
        list_of_log_files = getlogfiles(hr, minutes, logfilefilter)


    # print list_of_log_files

    ouputdir = props.get('output.file.dir')
    if not os.path.exists(ouputdir):
        os.makedirs(props.get('output.file.dir'))

    if os.path.exists(reportfilepath):
        bkpfile = reportfilepath+".bkp_"+str(int(time.time()))
        logger.info(reportfilepath+" already exists. Taking backup of the file to "+bkpfile)
        os.rename(reportfilepath, bkpfile)

    reportfile = open(reportfilepath, 'a+')
    for fpath in list_of_log_files:
        logger.info("Checking file : %s", fpath)
        fileutil.analyze(fpath, reportfile, list_of_keywords, excludes, limit, regex=None)
        logger.info("Finished checking file.")
    reportfile.close()

if __name__ == "__main__":
    cfg = "analyzer.properties"
    rep = "loganalyzerReport.txt"
    args = len(sys.argv)
    if args == 3:
        cfg = sys.argv[1]
        rep = sys.argv[2]
    elif args == 2:
        cfg = sys.argv[1]

    analyze(cfg, rep)
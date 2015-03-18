__author__ = 'Avinesh_Kumar'

import os
import time
import logging
import properties
import fileutil
import glob

propertiesfilepath = 'analyzer.properties'
default_regex = ['(^ERROR)', '^(?!INFO|DEBUG)(?:(?!.*class\.method).*\W*)(^.*Exception)(?:.*)']

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

reportfilepath = props.get('output.file.dir') + os.path.sep + "output-report" + str(int(time.time())) + ".txt"
logfilepat = props.get('log.file.pattern')
logfilefilter = dirpath + os.path.sep + logfilepat

hr = props.get('time.in.hr')
minutes = props.get('time.in.min')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logging.info('log base dir: %s', dirpath)
logging.info('time in hr: %s', hr)
logging.info('time in min: %s', minutes)
logging.info("file pattern: %s", logfilefilter)
# logging.info("files: %s",glob.glob(logfilefilter))
past = time.time()

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


print list_of_log_files

reportfile = open(reportfilepath, 'a+')
for fpath in list_of_log_files:
    logging.info("Checking file : %s", fpath)
    fileutil.analyze(fpath, reportfile, list_of_keywords, limit, regex=None)
    logging.info("Finished checking file.")
reportfile.close()
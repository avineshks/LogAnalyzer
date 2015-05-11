
Introduction:

A simple and flexible python tool to analyze multiple log files at once, it outputs number of lines before and below the occurrence of pattern in log files and also generate the stats about number of occurences of pattern in files. This will help in narrow down your effort to finding out relevent information. By default, it searches for Error and Exceptions in logs and generate report. Default report may be useful in indicating unusual behavior of application. 

Note: It is compatible only with Linux remote server. For remote windows machine, copy the log files using other tools and run the script in local mode- described later.

Steps to setup for windows:

1.	Download and Install python 2.7 for windows from here- https://www.python.org/downloads/release/python-279/
2.	Download and Install MS VC++ compiler for python 2.7 from http://www.microsoft.com/en-us/download/details.aspx?id=44266 
3.	Run this command from cmd- C:\Python27\Scripts\pip.exe install paramiko

Steps to setup for linux:

1.	Run this command-  pip install paramiko


You can skip the step if already done otherwise you should follow the steps as paramiko installation depends on MS VC++ compiler for windows only.

Instruction to run:
Pre-requisite: Put all files under one folder for remote mode described later.

Remoteloganalyzer has two mode: 1. Local 2. Remote 

1.	Local mode:   means your logs files are on same host from where you are executing script.
           
          python remoteloganalyzer.py local –c <configfilename> -r <reportfileName>
          For more check help using command -  python remoteloganalyzer.py local –h

2.	Remote mode:   means your logs files are on different host from where you are executing script.

          python remoteloganalyzer.py remote –i <ip> -u <user> -p <pass> –c <configfilename> -r <reportfileName>
          For more check help using command -  python remoteloganalyzer.py remote –h

You can check help to run the script using command: - python remoteloganalyzer.py –h

Properties File Help:

1.	log.file.dir --> path to directory which contains log files.  Make sure user (script owner) should have read permission on directory.

        log.file.dir=/your/logfiles/dir/

2.	log.file.pattern--> full name to include only one file or regex to include multiple files.

        log.file.pattern=yourproduct.log.*

3.	output.file.dir --> path to the directory which will contain generated reports. User (script owner) must have write permission for this directory.

        output.file.dir=/tmp/loggerAnalyzer-reports/

4.	pre.post.line.limit --> Number of lines, will be fetched before and after the regex occurrence.

        pre.post.line.limit=10

5.	search.keywords.seperator --> separator for search keywords. By default it will be comma - ,

6.	search.keywords --> [search.keywords.seperator] separated keywords or regex to search.

        search.keywords=
        Note: You may leave this empty if disable.default.search is false(0).
        
7.	exclude.keyword.list --> [search.keywords.seperator] separated keywords or regex to tell analyzer to exclude the line.

        exclude.keyword.list = class\.method,INFO,DEBUG
        Note: You may leave this empty.

8.	disable.default.search --> to disable the default search for Error and Exception that program has.

        Value 0 -> false
        Value 1 -> True
        disable.default.search=0

9.	time.in.hr --> hours. Analyzer will analyze the logs file generated in past one hour. Value 0 will disable this feature and enable the time.in.min feature.

        time.in.hr=1

10.	time.in.min --> minutes. Analyzer will analyze the logs file generated in past one minute.

        time.in.min=1


Usage Scenarios: 

1.	If you want to generate report for less than 1 hr. then use below combination:

        time.in.hr=0
        time.in.min=20


2.	If you want to generate report for last 1 hr. then use below combination:

        time.in.hr=1
        time.in.min=0

3.	I don’t want use time based selection of files, just want to apply filter [log.file.pattern] on files.

        time.in.hr=0
        time.in.min=0

4.	I want to search with my own regex only.

        disable.default.search=1
        search.keywords=message=Read 5 properties from DB,(^FATAL)

Note:  
1.	As program is properties driven, so set correct values to properties.


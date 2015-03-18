
Setting up:

1.	Copy the loganalyzer.zip to /tmp  directory on Linux box.
2.	Execute the command:-   unzip -o loganalyzer.zip ; cd loganalyzer
3.	Set up the analyzer.properties accordingly. See help.

Analyzing logs:

4.	Execute command:   python loganalyzer.py


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

7.	disable.default.search --> to disable the default search for Error and Exception that program has.

        Value 0 -> false
        Value 1 -> True
        disable.default.search=0

8.	time.in.hr --> hours. Analyzer will analyze the logs file generated in past one hour. Value 0 will disable this feature and enable the time.in.min feature.

        time.in.hr=1

9.	time.in.min --> minutes. Analyzer will analyze the logs file generated in past one minute.

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


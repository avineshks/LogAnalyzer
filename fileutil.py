import re
import logging

__author__ = 'Avinesh_Kumar'


def add(linebuffer, data, limit):
    if len(linebuffer) < limit:
        linebuffer.append(data)
    else:
        linebuffer.pop(0)
        linebuffer.append(data)


def analyze(inputfile, output, list_of_keywords=[], exclude_list=[], limit=10, regex=None):
    """
    inputfile  input file path
    output    output file object
    list_of_keywords   list of regex or keywords to search in input file. defaul: []
    limit   no of line fetch before and and after occurrence
    regex   regex to search
    :rtype : object
    """
    linebuffer = []  # DO Not Change
    prev_line_no = -1  # DO Not Change
    tot_line = 0  # DO Not Change
    keymapping = {}
    # exceptions = []
    # global tot_line
    # global prev_line_no
    # output = open(outputfile, 'a')
    output.write("\n start processing File: " + inputfile)
    output.write("\n------------------------------------------\n")
    f = open(inputfile, 'r')
    for index, line in enumerate(f):
        # addToList(line)
        # print "index:", index
        # print "line:", line
        tot_line = index
        result = 0
        if regex is not None:
            regexresult = re.search(regex, line)
            if regexresult:
                result = 1

        # print line
        # print "file checking regex...", list_of_keywords
        isinclude = 1
        size = len(line)
        for word in exclude_list:
            # print word
            if re.search(word, line) is not None:
                isinclude = 0
                break
        # print "done: ", isinclude

        if isinclude:
            for keyword in list_of_keywords:
                keywdres = re.search(keyword, line)
                 # print keywdres
                if keywdres is not None:
                    result = 1
                    grp = keywdres.groups()
                    if len(grp) == 1:
                        word = grp[0]
                        keymapping[word] = keymapping.get(word, 0) + 1
                    elif len(grp) > 1:
                        word = grp[1]
                        keymapping[word] = keymapping.get(word, 0) + 1
        # print "finished regex checking"

        if not regex and not list_of_keywords:
            output.write("No reports generated. Check the search criteria.\n")
            return

        if result:
            #print "result:", result
            for l in linebuffer:
                # print "buffer:", \
                output.write(l)
            del linebuffer[:]
            # print line
            output.write(line)
            prev_line_no = index
            # print "setting prev line no: ", prev_line_no
        else:
            if index - prev_line_no == limit:
                # print "in else if prev line no: ", prev_line_no
                # print "in else if  line no: ", index
                add(linebuffer, line, limit)
                if prev_line_no != -1:
                    for l in linebuffer:
                        # print "buffer:", l
                        output.write(l)

                del linebuffer[:]
                output.write('\n\n\n')
            else:
                # print "adding to list: ", line
                add(linebuffer, line, limit)
        if tot_line - prev_line_no < limit:
            for l in linebuffer:
                # print "buffer o:", l
                output.write(l)
            del linebuffer[:]

    if not len(keymapping):
        output.write("No result. Change the search criteria.")
        output.write("\n--------------------------------------------------------------\n")
        output.write("end of processing File: " + inputfile + "\n")
        output.write("----------------------------------------------------------------\n")
    else:
        output.write("\n--------------------------------------------------------------\n")
        output.write(" end of processing File: " + inputfile + "\n")
        output.write("------------------------------------------------------------------")
        output.write("\n\n\n======================== stats for " + inputfile + " =============================\n")
        output.write("keywords                :             no of occurences \n")
        output.write("------------------------------------------------------------------\n")
        for key, value in keymapping.iteritems():
            output.write(key + " : " + str(value))
            output.write('\n')
        output.write("======================== end stats =============================\n\n\n")
    f.close()


def main():
    ex = 'Exception'
    outputfile = open('output.txt', 'a+')
    analyze('exception.txt', outputfile)
    outputfile.close()


if __name__ == "__main__":
    main()
import re
import PropertiesReader
import logging

__author__ = 'Avinesh_Kumar'

linebuffer = []  # DO Not Change
prev_line_no = -1  # DO Not Change
tot_line = 0  # DO Not Change
keymapping = {}
exceptions = []


def add(data, limit):
    if len(linebuffer) < limit:
        linebuffer.append(data)
    else:
        linebuffer.pop(0)
        linebuffer.append(data)


def analyze(inputfile, output, list_of_keywords=[], limit=10, regex=None):
    """
    inputfile  input file path
    output    output file object
    list_of_keywords   list of regex or keywords to search in input file. defaul: []
    limit   no of line fetch before and and after occurrence
    regex   regex to search
    :rtype : object
    """
    global tot_line
    global prev_line_no
    # output = open(outputfile, 'a')
    output.write("\n start processing File: "+inputfile)
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

        for keyword in list_of_keywords:
            keywdres = re.search(keyword, line)
            if keywdres is not None:
                result = 1
                grp = keywdres.groups()
                if len(grp) == 1:
                    if not keymapping.get(grp[0]):
                        keymapping.__setitem__(grp[0], 1)
                    else:
                        count = keymapping.get(grp[0])
                        keymapping.__setitem__(grp[0], count + 1)
                elif len(grp) > 1:
                    if not keymapping.get(grp[1]):
                        keymapping.__setitem__(grp[1], 1)
                    else:
                        count = keymapping.get(grp[1])
                        keymapping.__setitem__(grp[1], count + 1)


        if not regex and not list_of_keywords:
            output.write("No reports generated. Check the search criteria.\n")
            return

        if result:
            # print result
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
                add(line, limit)
                if prev_line_no != -1:
                    for l in linebuffer:
                        # print "buffer:", l
                        output.write(l)

                del linebuffer[:]
                output.write('\n\n\n')
            else:
                # print "adding to list: ", line
                add(line, limit)
    if tot_line - prev_line_no < limit:
        for l in linebuffer:
            # print "buffer o:", l
            output.write(l)
        del linebuffer[:]

    if not len(keymapping):
        output.write("No result. Change the search criteria.")
        output.write("\n--------------------------------------------------------------\n")
        output.write("end of processing File: "+inputfile+"\n")
        output.write("----------------------------------------------------------------\n")
    else:
        output.write("\n--------------------------------------------------------------\n")
        output.write(" end of processing File: "+inputfile+"\n")
        output.write("------------------------------------------------------------------")
        output.write("\n\n\n======================== stats for "+inputfile+" =============================\n")
        output.write('keywords                :             no of occurences\n')
        output.write('------------------------------------------------------------------\n')
        sep = '  :  '
        for key, value in keymapping.iteritems():
            output.write(key + sep + str(value))
            output.write('\n')
        output.write("======================== end stats =============================\n\n\n")
    f.close()


def main():
    ex = 'Exception'
    outputfile = open('output.txt', 'a+')
    analyze('exception.txt', outputfile)
    # props = PropertiesReader.read(propertiesfilepath)
    # inpf = props.get('log.file.dir')
    # generate(inpf, outputfile)
    outputfile.close()


if __name__ == "__main__":
    main()
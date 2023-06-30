import re
import shutil
import time
from os import walk
import os


def write_parsed(file, req,resp):
    with open(where_to_save + '\\' + file, 'a', encoding="utf8") as f2:
        file2 = f2.write(req)
        if req != "": file2 = f2.write("\n\n")      #
        file2 = f2.write(resp)
        if resp != "": file2 = f2.write("\n\n")
        f2.close()
        time.sleep(1)


#################################################### CFG (start) ###########################################

Dumped_http_request = "Dumped HTTP request for"
Dumped_http_response = "Dumped HTTP response"
logo = "_______/ /"
where_to_report = "report"
where_to_save = ".\\report_parsed"
where_to_rez = ".\\rez"


flag_regima = 0 # for debug ness

#################################################### CFG (end) ###########################################


if not os.path.exists(where_to_save):
        os.makedirs(where_to_save)                                                                          #create folder if not created

list( map( os.unlink, (os.path.join( where_to_save,f) for f in os.listdir(where_to_save)) ) )              #delete old files in folder

if not os.path.exists(where_to_rez):
        os.makedirs(where_to_rez)                                                                          #create folder if not created

list( map( os.unlink, (os.path.join( where_to_rez,f) for f in os.listdir(where_to_rez)) ) )

ff = []                                                                                                 #create list for collect all files from nuclei result
for (dirpath, dirnames, filenames) in walk(where_to_report):
        ff.extend(filenames)                                                                            # read filename in folder of nulei result
        break
for g in range(len(ff)):
        ff[g] = ff[g].replace('.txt', '')                                                                       # delete extensions, for add _parsed.txt to the end of filename

with open(where_to_report + '\\' + ff[0] + '.txt', 'r', encoding="utf8") as f:
        file = f.read()
        f.close()

if flag_regima == 0:

    r = ["POST", "GET", "OPTIONS", "TRACE", "HEAD", "PUT"]                                              # BORED TO WRITE COMMENTS FURSER
    req = []
    ans = []
    rez_time_look = ""
    pos1 = 1
    pos0 = 1
    g = 0
    i = 0
    while g < len(ff):
        with open(where_to_report + "\\" + ff[g] + ".txt", 'r', encoding="utf8") as f2:

            file2 = f2.read()
            f2.close()
            time.sleep(1)

            tmp = file2
            for y in r:

                while pos1 > 0:
                    pos0 = tmp.find(y)
                    if pos0 == -1:
                        break
                    pos1 = tmp.find("HTTP/1.1 ", pos0)
                    pos2 = tmp.find("\n\n", pos1)
                    pos3 = tmp.find("\n\n", pos2 + len("HTTP/1.1 "))
                    if pos1 != -1 or pos2 != -1 or pos3 != -1:

                        req_ans = tmp[pos0:pos3]
                        req.append(tmp[pos0:pos1])
                        ans.append(tmp[pos1:pos3])
                        pos4 = ans[i].find("dsl-")
                        if pos4 != -1:
                            rez_time_look = rez_time_look + "\n\n+++++++++++++++++++++++\n\n" + req[i] + "\n" + ans[i] + "\n"

                        i = i + 1
                        tmp = tmp[pos3:]

            print("Working " + ff[g] + " looking for times done")
            g = g + 1

    with open(where_to_rez + "\\rez_time.txt", 'w', encoding="utf8") as f2:
        f2.write("")
        f2.write(rez_time_look)
        time.sleep(1)
        f2.close()

    req = []
    ans = []
    file = file[file.index(Dumped_http_request):]

    #file = file[file.index("\n\n")+2:]
    #l = [match.start() for match in re.finditer(Dumped_http_request,file)]
    #d = [match.start() for match in re.finditer(Dumped_http_response,file)]
    #text = file[l[0]:l[1]]
    #text= text[text.index(Dumped_http_response)-80:]


    file = file[file.index("POST"):]
    req = file[:file.index("\n[")]
    #print(req)

    l = len(req)
    file = file[l:]
    resp = file[file.index("HTTP/1.1 "):]
    resp = resp[:resp.index("\n[")]
    #print(resp)

    write_parsed(ff[0] + '_parsed.txt',req,resp)  # Delete FIRST LOGO

    count_responses_equal = file.index(resp)
    tmp2 =""
    g = 0

    while g < len(ff):
        with open(where_to_save + '\\' + ff[g] + '_parsed.txt', 'w', encoding="utf8") as f2:
            file2 = f2.write("")                                                                                #create new parsed file
            f2.close()
            time.sleep(1)
        with open(where_to_report + '\\' + ff[g] + '.txt', 'r',encoding="utf8") as f:
            text = f.readlines()
            i = 0
            pp = len(text)
            rez = ""
            while i < len(text):
                tmp = text[i]

                if tmp.find("POST")  != -1 or tmp.find("GET") != -1:
                    while tmp.find(Dumped_http_response) == -1 and tmp.find("No results found") == -1 and i < len(text) - 1 :
                        tmp2 = tmp2 + tmp
                        i = i + 1
                        tmp = text[i]
                    #tmp2 = tmp2 + "\n"
                    #print(tmp2)
                    rez = rez + tmp2 + "\n" #write_parsed(ff[g] + '_parsed.txt',tmp2, "")
                    tmp2 = ""
                if tmp.find("HTTP/1.1 ") != -1:
                    while tmp.find(Dumped_http_request) == -1 and tmp.find("No results found") == -1 and i < len(text) - 1:
                        tmp2 = tmp2 + tmp                                                                                   # Get request|answer and write to pure file
                        i = i + 1
                        tmp = text[i]
                    #tmp2 = tmp2 + "\n"
                    #print(tmp2)
                    rez = rez + tmp2 + "\n" #write_parsed(ff[g] + '_parsed.txt', "", tmp2)
                    tmp2 = ""
                i = i + 1

            f.close()

        write_parsed(ff[g] + '_parsed.txt', "", rez)
        print("Parsing " + ff[g] + " for pure rezults")
        g = g + 1


flag_regima = 1

with open(where_to_rez + "\\rez_methods_all.txt", 'w', encoding="utf8") as f2:
    f2.write("")
    f2.close()

if flag_regima == 1:

    ff = []  # create list for collect all files from parsed result
    for (dirpath, dirnames, filenames) in walk(where_to_save):
        ff.extend(filenames)  # read filename in folder of nulei result
        break
    g = 0
    rez_with_all_methods = ""
    rez_with_len_all = ""
    rez_with_len = []
    while g < len(ff):
        with open(where_to_save + "\\" + ff[g], 'r', encoding="utf8") as f2:

            file2 = f2.read()
            f2.close()
            time.sleep(1)


            with open(where_to_rez + "\\rez_methods_all.txt", 'a', encoding="utf8") as f2:
                f2.write("\n")

                rez_with_all_methods = rez_with_all_methods + "In "+ ff[g] + "\n\nTHERE ARE " + str(file2.count("POST")) + " POST requests" + "\n"
                rez_with_all_methods = rez_with_all_methods + "THERE ARE " + str(file2.count("GET")) + " GET requests" + "\n"
                rez_with_all_methods = rez_with_all_methods + "THERE ARE " + str(file2.count("OPTIONS")) + " OPTIONS requests" + "\n"
                rez_with_all_methods = rez_with_all_methods + "THERE ARE " + str(file2.count("TRACE")) + " TRACE requests" + "\n"
                rez_with_all_methods = rez_with_all_methods + "THERE ARE " + str(file2.count("HEAD")) + " HEAD requests" + "\n"
                rez_with_all_methods = rez_with_all_methods + "THERE ARE " + str(file2.count("PUT")) + " PUT requests" + "\n"

                f2.write(rez_with_all_methods)
                time.sleep(1)
                f2.close()


            r = ["POST","GET","OPTIONS","TRACE","HEAD","PUT"]
            req = []
            ans = []
            cl = []
            tmp = file2

            i = 0
            pos1 = 1
            pos0 = 1
            for y in r:

                while pos1 > 0:
                    pos0 = tmp.find(y)
                    if pos0 == -1:
                        break
                    pos1 = tmp.find("HTTP/1.1 ",pos0)
                    pos2 = tmp.find("\n\n",pos1)
                    pos3 = tmp.find("\n\n", pos2+len("HTTP/1.1 "))

                    req_ans = tmp[pos0:pos3]
                    req.append(tmp[pos0:pos1])
                    ans.append(tmp[pos1:pos3])
                    cl_num = ans[i][ans[i].find("Content-Length: ") + len("Content-Length: "):ans[i].find("\n",ans[i].find("Content-Length: "))]
                    cl.append(cl_num)
                    i = i + 1
                    tmp = tmp[pos3:]

                    # finding times
                   # rez_time_boom = time_look(req,ans)


                pos1 = 1
                tmp = file2 # back the whole text

            duplicate_elements = {}
            for item in cl:
                if item in duplicate_elements:
                    duplicate_elements[item] += 1
                else:
                    duplicate_elements[item] = 1

            print(duplicate_elements)

        i = 0
        for y in duplicate_elements:
            while i < len(ans):
                pos0 = ans[i].find("Content-Length: "+ y)
                if pos0 != -1:
                    rez_with_len.append(req[i] + "\n" + ans[i])
                    i = 0
                    break
                i = i + 1
        i = 0
        for y in duplicate_elements:
            #print("\n++++++++++++++++++++++++++++ " + "Uniq len with: " + y + " +++++++++++++++++++++++++++++++++\n")
            #print(rez_with_len[i])
            i = i + 1
        i = 0

        print("Done with len in file  " + ff[g])

        for t in rez_with_len:
            rez_with_len_all = rez_with_len_all + "\n\n+++++++++++++++++++++++++++\n\n" + t + "\n"

        with open(where_to_rez + "\\rez_len_"+ff[g]+".txt", 'w', encoding="utf8") as f2:
            f2.write("")
            f2.write(rez_with_len_all)
            f2.close()

        rez_with_len_all = ""
        rez_with_all_methods = ""
        rez_with_len = []
        g = g + 1

flag_regima = 2

if flag_regima == 2:

    ff = []  # create list for collect all files from nuclei result
    for (dirpath, dirnames, filenames) in walk(where_to_report):
        ff.extend(filenames)  # read filename in folder of nulei result
        break
    g = 0
    rez_with_all_status = ""
    rez_with_status = []
    req_ans = ""
    while g < len(ff):
        with open(where_to_report + "\\" + ff[g], 'r', encoding="utf8") as f2:

            file2 = f2.read()
            f2.close()
            time.sleep(1)

            r = ["301", "500", "501", "502", "503", "101", "302"]
            req = []
            ans = []
            cl = []
            tmp = file2
            req_ans = req_ans + "\n+++++++++++++++++++++" + " for " + ff[g] + "++++++++++++++++++++++++++\n"
            i = 0
            pos1 = 1
            pos0 = 1
            for y in r:

                while pos0 > 0:
                    pos0 = tmp.find("HTTP/1.1 " + y)
                    if pos0 != -1:
                        pos1 = tmp.rfind("Dumped HTTP request", 0, pos0)
                        pos2 = tmp.find("Dumped HTTP request", pos0)
                        if pos2 == -1:
                            print("Cannot find the next request")
                            pos2 = len(tmp)
                        req_ans = req_ans + tmp[pos1:pos2]
                        tmp = tmp[pos0+len(y):]


                pos0 = 1
                tmp = file2 # back the whole text
            print("Done with strange status in file  " + ff[g])

        g = g + 1

    print(req_ans)
    with open(where_to_rez + "\\rez_strange_status" + ".txt", 'w', encoding="utf8") as f2:
        f2.write("")
        f2.write(req_ans)
        f2.close()

print("!!!!!!!!!!!!!!!!DONE!!!!!!!!!!!")








import re,os
import argparse
import requests
import logging


parser = argparse.ArgumentParser()
parser.add_argument("-u","--url",
                        help="Single url from weburls.txt")
parser.add_argument("-t","--targetname",
                        help="Targets friendly name")

args = parser.parse_args()

if(args.targetname==None or args.url==None):
    parser.print_help()
    exit()


end_point = []

#more can be added, as requirement
extension=(".json",".js",".php",".xml",".asp",".aspx",".do",".jsp",".jspx",".htm",".html")
start = ("/","//","http://","https://","file://","php://","ftp://","./","../","ws://","wss://")

def end_points(content):
    for i in content:
        if re.match("^[a-zA-Z0-9_\/:&?%.\-=]*$", i):
            if (i.startswith(start) or i.endswith(extension)):
                end_point.append(i)


    for i in content:
        if re.match("^[a-zA-Z0-9_\/:&?%.\-=]*$", i):
            if (not i.startswith(start)):
                temp = i.split("/")
                if "/"+temp[0] in end_point or "./"+temp[0] in end_point or "../"+temp[0] in end_point:
                    end_point.append(i)

def saving_in_file(end_point,filepath):
    with open(os.path.join(filepath,"endpoints.txt"),'a') as f:
        f.write(end_point)
        f.write("\n")

#To use with burl for second level takeover
def saving_in_file2(end_point,filepath):
    with open(filepath,'a') as f:
        f.write(end_point)
        f.write("\n")

def print_end_points(end_point,filepath):
    start1=("http://","https://","file://","php://","ftp://","ws://","wss://","//")
    a="\n-----------------Remote files which are added-----------------------------------\n"
    saving_in_file(a,filepath)
    for i in end_point:
        if i.startswith(start1):
            saving_in_file(i,filepath)
            saving_in_file2(i,"results/{0}/stko/urls.txt".format(args.targetname))

    b="\n-----------------These files are present in server------------------------------\n"
    saving_in_file(b,filepath)
    for i in end_point:
        if i.endswith(extension):
            saving_in_file(i,filepath)

    c="\n-----------------These are files and directory, you can look into---------------\n"
    saving_in_file(c,filepath)
    start1=("/","./","../")
    for i in end_point:
        if i.startswith(start1) and not (i.endswith(extension)):
            saving_in_file(i,filepath)


    for i in end_point:
        if(not i.startswith(start) and not i.endswith(extension)):
            saving_in_file(i,filepath)


def main():
    targetname = args.targetname
    url = args.url.replace('.','_').replace('/','_').replace(':','_')

    jsfolder = "results/{0}/javascript/{1}".format(targetname,url)

    logfilename = 'results/{0}/log.txt'.format(targetname)  #Log to file instead
    logging.basicConfig(
        level = logging.INFO, 
        format='%(asctime)s : %(message)s',
        datefmt='%d/%m/%Y %H:%M',
        filename=logfilename)

    if not os.path.exists("results/{0}/stko".format(targetname)):
        os.mkdir("results/{0}/stko".format(targetname))

    if os.path.exists(jsfolder):
        for filename in os.listdir(jsfolder):
            file = os.path.join(jsfolder,filename)
            if not file.endswith('.txt'):
                with open(file) as f:
                    logging.info("[+] Extracting endpoints from {0}".format(file))
                    end_points(f.read().split('"'))
        print_end_points(set(end_point),jsfolder)
    else:
        logging.info('[!] Folder not exist : {0}'.format(jsfolder))


if __name__=='__main__':
    main()

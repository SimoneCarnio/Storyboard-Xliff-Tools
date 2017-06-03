import os.path
import re
import glob
from slugify import slugify

my_path = os.path.abspath(os.path.dirname(__file__))

source_path = os.path.join(my_path, "*.m")
strings_path = os.path.join(my_path, "processed.strings")



pattern_ok = r'(@\"([^\"]{1,})\")'

# automatic filtering, not implemeted yet
# pattern_no = []
# pattern_no.append("NSLocalizedString\(@\"([^\"]{2,})\"[\s\,]*@\"([^\"]{2,})\"\)")


class bcolors:
    HEADER = '\033[91m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def partial_replace(match, edit):
    if (edit):
        inp = raw_input("Replace ? " + bcolors.OKBLUE + match.group(2) + bcolors.ENDC + " y/[n]: ")
        if inp == "" or inp == "n":
            result = match.group(1)
        else:
            result = 'NSLocalizedString(@"' + slugify( match.group(2)) + '", nil)'
            strings.write('"' + slugify( match.group(2)) + '" = "' +  match.group(2) + '";'+ "\r" )
    else:
        result = bcolors.HEADER +  match.group(1) + bcolors.ENDC
    return result


strings = open(strings_path, "w")

filelist = glob.glob(os.path.join(source_path))
for file in filelist:
    print bcolors.FAIL + bcolors.BOLD + file +  bcolors.ENDC + "\r\r";
    if not os._exists(file+".backup"):
        os.rename(file, file+".backup")
        newfile = open(file, "w")
        with open(file+".backup") as fp:
            for line in fp:
                coloredline = re.sub(pattern_ok, lambda m: partial_replace(m, False)  , line.rstrip())
                if (coloredline != line.rstrip()):
                    print coloredline
                    line = re.sub(pattern_ok, lambda m: partial_replace(m, True)  , line.rstrip())
                newfile.write(line.rstrip() + "\r")
        newfile.close()



strings.close()

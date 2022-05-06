import graph
import sys
from os.path import exists
from enum import Enum

# CONSOLE FORMAT STYLING VALUES
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# CUSTOM ERROR TYPES
class Error(Enum):
    FILE_INCORRECT_FORMAT = 1
    FILE_NOT_FOUND = 2
    INCORRECT_AMOUNT_ARGS = 3
    ARG2_TO_ARG4_NOT_CORRECT = 4
    TOO_MANY_KCORES = 5

## FUNCTIONS

# Return the index of the first array which is not empty inside of a two dim array
# Ex : [[],[],[5],[5,6,7]] return 2
# Ex : [[]] return -1
def twoDimArrayIndexHelper(twoDimArray):
    index = 0
    empty = True
    while(empty):
        empty = len(twoDimArray[index]) == 0
        index+=1
    index-=1
    if empty:
        return -1
    else:
        return index

# Reads from a file and makes a graph object out of it.
def readGraph(path):
    g = graph.Graph()

    if not exists(path):
        sys.exit(errorMessage(Error.FILE_NOT_FOUND))
    file = open(path,"r")

    lines = file.readlines()
    if(lines[0].strip() != "% sym unweighted"):
        sys.exit(errorMessage(Error.FILE_INCORRECT_FORMAT))
    for line in lines:
        if line[0] != "%":
            g.addEdge(tuple(int(i) for i in line.split()))
    return g

def helpCommand():
    return f"""
    This application allows any user to check the Degeneracy and Coloration of any graph,
    using a naive degeneracy algorithm, Matula & Beck algorithm and DSATUR.
    
    {BOLD}----- ARGUMENTS{ENDC}
    
    You can include either ZERO (0), ONE (1) or FOUR (4) arguments by using :
    \t{WARNING}python3 main.py {UNDERLINE}arg1 arg2 arg3 arg4{ENDC}
    
    {OKBLUE}arg1 [optional]{ENDC}
    \tThe path of the file containing the graph. It can be relative or absolute.
    \t{FAIL}The file has to be in KINECT format.
    \tThe graph has to be undirected, unweighted, with no multiple edges.
    \tThis is indicated by the "% sym unweighted" at the beginning of the file.
    \t{BOLD}If those conditions are not met, the application might not work correctly.{ENDC}
    \t{OKGREEN}Default value : {UNDERLINE}./graphes/data_small{ENDC}
    
    {OKBLUE}arg2 [optional]{ENDC}
    \tSet arg2 to 0 to not display anything
    \tSet arg2 to 1 to display degeneracy with naive algorithm
    \tSet arg2 to 2 to also display the k-cores
    \t{OKGREEN}Default value : {UNDERLINE}1{ENDC}

    {OKBLUE}arg3 [optional]{ENDC}
    \tSet arg3 to 0 to not display anything
    \tSet arg3 to 1 to display degeneracy with Matula & Beck algorithm
    \tSet arg3 to 2 to also display the k-edges
    \t{OKGREEN}Default value : {UNDERLINE}0{ENDC}

    {OKBLUE}arg4 [optional]{ENDC}
    \tSet arg4 to 0 to not display anything
    \tSet arg4 to 1 to display coloration with DSATUR algorithm
    \tSet arg4 to 2 to also display the color of each vertex
    \t{OKGREEN}Default value : {UNDERLINE}0{ENDC}

    {BOLD}----- GRAPH FILE{ENDC}

    The graph has to be retrieved from {UNDERLINE}http://konect.cc/networks/{ENDC}
    Make sure the first line of the file is '% sym unweighted'
    and that each line not starting with '%' contains only 2 integers
    
    {OKBLUE}Correct file example :{ENDC}
    {WARNING}% sym unweightesd
    1 2
    1 3
    2 3
    1 4
    2 4
    3 4
    1 5{ENDC}
    """

def errorMessage(err):
    if (err == Error.FILE_INCORRECT_FORMAT) :
        return f"""
        {FAIL}{BOLD}ERROR : Your file has been read, but is not formated correctly.{ENDC}
        {WARNING}The graph has to be retrieved from {UNDERLINE}http://konect.cc/networks/{ENDC}
        {WARNING}Make sure the first line of the file is '% sym unweighted'
        and that each line not starting with '%' contains only 2 integers
        
        Correct file example :
        % sym unweightesd
        1 2
        1 3
        2 3
        1 4
        2 4
        3 4
        1 5{ENDC}"""

    if (err == Error.FILE_NOT_FOUND) :
        return f"""
        {FAIL}{BOLD}ERROR : Your file has not been found{ENDC}
        {WARNING}Make sure you pass the correct relative or absolute path for your file{ENDC}"""
    
    if (err == Error.INCORRECT_AMOUNT_ARGS) :
        return f"""
        {FAIL}{BOLD}ERROR : Incorrect amount of arguments{ENDC}
        {WARNING}Make sure there are either zero (0), one (1) or four (4) arguments{ENDC}"""

    if (err == Error.ARG2_TO_ARG4_NOT_CORRECT) :
        return f"""
        {FAIL}{BOLD}ERROR : Incorrect second, third and fourth arguments{ENDC}
        {WARNING}Make sure you those 3 arguments are integers between 0 and 2 included. For exemple 2 1 1{ENDC}"""

    if (err == Error.ARG2_TO_ARG4_NOT_CORRECT) :
        return f"""
        {FAIL}{BOLD}ERROR : Too many KCores (greater than 300){ENDC}
        {WARNING}Either you graph is too big (but it is EXTREMELY unlikely), either there is an error in the Degeneracy algorithm{ENDC}"""
    


def args():
    ARG_DEGEN = 1
    ARG_MATULA = 0
    ARG_DSATUR = 0
    ARG_PATH_GRAPH = "./graphes/data_small"

    if len(sys.argv) != 2 and len(sys.argv) !=5:
        print("HERE")
        sys.exit(errorMessage(Error.INCORRECT_AMOUNT_ARGS))

    if(len(sys.argv) >=2 ):
        if(sys.argv[1] == "help"):
            sys.exit(helpCommand())
        else:
            ARG_PATH_GRAPH = sys.argv[1]

        if(len(sys.argv) == 5):
            arg2,arg3,arg4 = int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])

            if(arg2 in range (0,3) and arg3 in range (0,3) and arg4 in range (0,3)):
                ARG_DEGEN = int(arg2)
                ARG_MATULA = int(arg3)
                ARG_DSATUR = int(arg4)
            else:
                sys.exit(errorMessage(Error.ARG2_TO_ARG4_NOT_CORRECT))
        
    return (ARG_DEGEN,ARG_MATULA,ARG_DSATUR,ARG_PATH_GRAPH)
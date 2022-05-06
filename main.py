from ast import arg
import utils


## COMMAND LINE ARGUMENTS

ARG_DEGEN,ARG_MATULA,ARG_DSATUR,ARG_PATH_GRAPH = utils.args()

## MAIN

z = utils.readGraph(ARG_PATH_GRAPH)

print(f"\n\n{utils.OKGREEN}--- {utils.BOLD}RESULTS -------------------------{utils.ENDC}\n")

if(ARG_DEGEN != 0):
    (degen,centres) = z.degeneracy()
    print(f"{utils.BOLD}Degenerancy :{utils.ENDC}",str(degen))
    if(ARG_DEGEN == 2):
        print(f"\n{utils.BOLD}K-cores :{utils.ENDC}",centres)
    if(ARG_MATULA or ARG_DSATUR):
        print("\n----------\n")
    

if(ARG_MATULA != 0):
    (degenMB,verticesMB) = z.matulaBeckDegeneracy()
    print(f"{utils.BOLD}Matula & Beck Degeneracy :{utils.ENDC}",str(degenMB))
    if(ARG_MATULA==2):
        print(f"\n{utils.BOLD}Matula & Beck output vertices :{utils.ENDC}",verticesMB)
    if(ARG_DSATUR):
        print("\n----------\n")

if(ARG_DSATUR != 0):
    (chromaticNb,colors) = z.dsatur()
    print(f"{utils.BOLD}Chromatic Number :{utils.ENDC}",str(chromaticNb))
    if(ARG_DSATUR == 2):
        print(f"\n{utils.BOLD}Colors :{utils.ENDC}",colors)
    print("")
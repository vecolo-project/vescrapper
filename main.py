from ply4ever.evalTree import *
from ply4ever.consoleColor import bcolors
import ply.yacc as yacc

print(f"""
{bcolors.HEADER+bcolors.BOLD}Welcome to Vescrapper! Enter the search you want{bcolors.ENDC}
{bcolors.BOLD}------------------------------------------------{bcolors.ENDC}
Enter {bcolors.OKGREEN}exit();{bcolors.ENDC} to leave
Enter {bcolors.OKGREEN}debugOn();{bcolors.ENDC} to show treeGraph {bcolors.WARNING}(must have graphviz installed){bcolors.ENDC}
Enter {bcolors.OKGREEN}debugOff();{bcolors.ENDC} to disable treeGraph showing (default)
{bcolors.BOLD}------------------------------------------------{bcolors.ENDC}
{bcolors.BOLD+bcolors.UNDERLINE}Command you can use :{bcolors.ENDC}
{bcolors.OKCYAN}GET [text|image] OF <term> FROM <source> WITH [<conditional terms>]? LIMIT <number>?;{bcolors.ENDC}

{bcolors.BOLD+bcolors.UNDERLINE}Examples:{bcolors.ENDC}
- {bcolors.OKBLUE}GET text,image OF rockrider FROM decathlon WITH ("ST 100" OR "ST 530 S") AND ("NOIR" OR "ROUGE") LIMIT 10;{bcolors.ENDC}
- {bcolors.OKCYAN}GET text OF rockrider FROM decathlon WITH "ST 100" LIMIT 10;{bcolors.ENDC}
- {bcolors.OKCYAN}GET image OF rockrider FROM go-sport LIMIT 5;{bcolors.ENDC}
""")

yacc.yacc()

# load_files(yacc)
cli(yacc)

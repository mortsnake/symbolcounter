# symbolcount.py
# Written by Ian Patterson
#
# Counter of various symbols, letters, and ASCII characters
# Storer of various JSON files
# Collector of not very useful data
# 
# Originally made to see how to set up my keyboard profile for my 40% layout Vortex Core
# I wanted to see which symbols I use the most while programming so I can set up my keybindings different.
# Maybe it's useful to someone else.

###################
# PROGRAM IMPORTS #
###################
import string
import json
import os
import sys
from signal import signal, SIGINT
from time import sleep

########################
# INI / CONFIG OPTIONS #
########################
# DATA_SCAN_TYPE
# What to look for/count in the files
#
# Options:
#   'printable' - All ASCII characters, symbols, whitespace, and hex-codes
#   'ascii_letters' - All letters, upper- and lowercase (a-z, A-Z)
#   'ascii_lowercase' - Lowercase letters (a-z)
#   'ascii_uppercase' - Uppercase letters (A-Z)
#   'digits' - Numbers (0-9)
#   'punctuation' - All punctuation/symbols (!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~) *DEFAULT*
DATA_SCAN_TYPE = 'punctuation'

# INPUT_TYPE
# How to look for the files
#
# Options:
#   'auto' - 'Automatically scans folder specified in SCAN_DIR *DEFAULT*
#   'manual' - Manually enter in locations/names of each file to scan
INPUT_TYPE = 'auto'

# SCAN_DIR
# Where to look for the files
#
# Options:
#   '' OR './' - Current Directory
#   './scanfiles/' - Subdirectory of current directory *DEFAULT*
#   'SOME/OTHER/PATH/' - Absolute path of your choosing
SCAN_DIR = './scanfiles/'

# JSON_LOCATION
# Where to look for/store the JSON output 
#
# Options:
#   '' OR './' - Current Directory
#   './resultfiles/' - Subdirectory of current directory *DEFAULT*
#   'SOME/OTHER/PATH/' - Absolute path of your choosing
JSON_LOCATION = './resultfiles/'

#####################
# PROGRAM FUNCTIONS #
#####################
# findOccurrences(string, char)
# Returns: array
# 
# Enumerates a string, returns array of index positions each time a character is in a string
# https://stackoverflow.com/questions/13009675/find-all-the-occurrences-of-a-character-in-a-string
def findOccurrences(s, ch): 
    return [i for i, letter in enumerate(s) if letter == ch]

# countOccurrences(string, char)
# Returns: integer
#
# Calls findOccurrences and the returns the total count
def countOccurrences(s, ch):
    arr = findOccurrences(s, ch)
    return len(arr)

# sigintHandler(signal, frame)
# Returns: Nothing
#
# Calls formatJSON, then exits the program.
def sigintHandler(signal_received, frame):
    formatJSON(runCount, symbolInfo)
    sys.exit(0)

# formatJSON(integer, dictionary)
# Returns: nothing
#
# Displays a formatted table of all objects searched for, sorted by number of hits found in files scanned
def formatJSON(runCount, symbolInfo):
    # After the user is done running the script, re-count the symbolInfo and display neatly
    sortedSymbolInfo = sorted(symbolInfo.items(), key=lambda x: x[1], reverse=True)

    print("\n\n")
    print("Number of Files Scanned:",runCount)

    print("Most Commonly Used Symbols:")
    for pair in sortedSymbolInfo:
        print("\t{}\t{}\t({:.1f} per document on average)".format(pair[0], pair[1], (pair[1] / runCount)))
       
    input("Press Enter to Exit")


#####################
# PROGRAM EXECUTION #
#####################
# Get the dir that the script is in, use that as a relative path
os.chdir(os.path.dirname(sys.argv[0]))

# Announce Global Variables
runCount = 0
symbolInfo = {}

# Organize the symbols into a list called 'symbolList'
symbolList = list(eval("string."+DATA_SCAN_TYPE))
print("Searching for Character List: ")
print(symbolList)

if not os.path.exists(SCAN_DIR):
    os.mkdir(SCAN_DIR)
    print("NO SCAN_DIR FOUND!  If this is the first time running this program, this directory has just been created for you!")
    print("\nPlease change one of the following settings in this program:")
    print("\t1) Fill the 'SCAN_DIR' directory listed with files to scan")
    print("\t2) Point the 'SCAN_DIR' directory to the folder you intend to scan")
    print("\t3) Change 'INPUT_TYPE' to manual in order to specify the location of each file you wish to scan")
    print("\n After something has been changed, please re-run this program.")
    input("\nPress ENTER to exit program.")
    sys.exit(-1)
if not os.path.exists(JSON_LOCATION):
    os.mkdir(JSON_LOCATION)

# Create loop to run program a bunch
if INPUT_TYPE == 'manual':
    end = 999999
else:
    end = len(os.listdir(SCAN_DIR))
    filesArray = os.listdir(SCAN_DIR)

# Display amount of iterations and break condition to user
print("***NOTICE***")
print("This program will loop for",str(end),"iterations, or until CTRL+C is pressed.\n\n")
sleep(1)

for run in range (0, end):
    # Declare variables for the parsing of JSON data
    jsonData = {}

    # First open the JSON file with all stats
    if os.path.exists(JSON_LOCATION+'runningTotal_'+DATA_SCAN_TYPE+'.json'):
        with open(JSON_LOCATION+'runningTotal_'+DATA_SCAN_TYPE+'.json', 'r') as jsonread:
            # Read the JSON file
            jsonData = json.load(jsonread)

            # Grab the current runCount
            runCount = jsonData['runCount'] + 1
            symbolInfo = jsonData['symbolInfo']

    else: # If the file doesn't exist, then will set the variables defined above to defaults, and create the JSON file
        runCount = 0
        jsonData['runCount'] = runCount
        jsonData['symbolInfo'] = {}

        for char in symbolList:
            jsonData['symbolInfo'][char] = 0

        with open(JSON_LOCATION+'runningTotal_'+DATA_SCAN_TYPE+'.json', 'w') as jsonwrite:
            json.dump(jsonData, jsonwrite, indent=4)

    if INPUT_TYPE == 'manual': # Open a user defined file, read the lines
        fin = input("Enter file to scan: ")
    else: # Scan the dir for all file names
        fin = SCAN_DIR+filesArray[run]

    fread = open(fin, 'r')
    freadLines = fread.readlines()

    # Increment runCount
    jsonData['runCount'] = runCount

    # Scan each line of file, count how many times each symbol appears, then add in the data to the JSON variable
    for line in freadLines:
        for symbol in symbolList:
            hits = countOccurrences(line, symbol)
            jsonData['symbolInfo'][symbol] += hits

    # As of this point, all information is stored in JSON array, so just need to re-write the data to runningTotal_DATA_SCAN_TYPE.json
    with open(JSON_LOCATION+'runningTotal_'+DATA_SCAN_TYPE+'.json', 'w') as jsonwrite:
        json.dump(jsonData, jsonwrite, indent=4)

# Run formatJSON to display all data after the loops have been completed
formatJSON(runCount, symbolInfo)
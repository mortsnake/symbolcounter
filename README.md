# symbolcounter.py
>Written by Ian Patterson  
  
>Counter of various symbols, letters, and ASCII characters.  
>Storer of various JSON files. 
>Collector of not very useful data. 


## What this is
Originally made to see how to set up my keyboard profile for my 40% layout Vortex Core, I wanted to see which symbols I use the most while programming so I can set up my keybindings different.  
Maybe it's useful to someone else.  

## How to use
1. Download the python file  
2. Run the python file: `python symbolcounter.py`  
The first run creates the directory to put the files you want to analyze in  

3. Fill the scan directory with files you want to count symbols, letters, numbers, or all ASCII characters with  
4. Run the program again  
5. OPTIONAL: Edit config settings inside the script to change behavior  

## Configuration settings  
```
DATA_SCAN_TYPE
What to look for/count in the files

Options:
  'printable' - All ASCII characters, symbols, whitespace, and hex-codes
  'ascii_letters' - All letters, upper- and lowercase (a-z, A-Z)
  'ascii_lowercase' - Lowercase letters (a-z)
  'ascii_uppercase' - Uppercase letters (A-Z)
  'digits' - Numbers (0-9)
  'punctuation' - All punctuation/symbols (!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~) *DEFAULT*
DATA_SCAN_TYPE = 'punctuation'
```   

```
INPUT_TYPE
How to look for the files

Options:
  'auto' - 'Automatically scans folder specified in SCAN_DIR *DEFAULT*
  'manual' - Manually enter in locations/names of each file to scan
INPUT_TYPE = 'auto'
```   

```
SCAN_DIR
Where to look for the files

Options:
  '' OR './' - Current Directory
  './scanfiles/' - Subdirectory of current directory *DEFAULT*
  'SOME/OTHER/PATH/' - Absolute path of your choosing
SCAN_DIR = './scanfiles/'
```   

```
JSON_LOCATION
Where to look for/store the JSON output 

Options:
  '' OR './' - Current Directory
  './resultfiles/' - Subdirectory of current directory *DEFAULT*
  'SOME/OTHER/PATH/' - Absolute path of your choosing
JSON_LOCATION = './resultfiles/'
```   

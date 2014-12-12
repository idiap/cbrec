############################################################################

              Content-Based Recommendation Generator (CBRec v1.0)      

############################################################################


README:
=======
A Python library which generates content-based recommendations for a set of 
items described by textual metadata using four possible vector space methods,
namely TF-IDF, LSI, RP and LDA. The library can be used in command line or 
directly in a Python program. It takes as input a JSON file which contains
an array of hashes that describe the metadata of items and generates an out-
put JSON file which contains the same item hashes augmented with two more att-
ributes, namely (i) rec attribute which contains the top-N recommendations for 
each item, represented by an array of item IDs and (ii) rec_scores attribute
which contains the top-N similarity scores, represented by an array of float
numbers.

FILES:
======
The library contains the following files:
   
    data.py           Data class for items (text extraction, preprocessing)
    vector_space.py   Vector space class supporting TF-IDF, LSI, RP and LDA
    generate.py       Main class responsible for genereting recommendations
    utils.py          Unbuffered stdout class
    example.json      Example JSON file with 1000 TED talks

USAGE:
======
Usage:
    generate.py --input=<path> --output=<path> [options]

Options:
    -v, --version                      show program's version number and exit
    -h, --help                         show this help message and exit
    -d, --debug                        print status and debug messages [default: False]
    -r, --display                      display recommendations per item [default: False]
    -i, --input=<path>                 path to JSON file to be used as input
    -o, --output=<path>                path to JSON file to be used as output
    --extract=<attributes>             comma separated JSON attributes to be used [default: All]
    --preprocess                       whether to preprocess text or not  [default: False]
    --method=<TFIDF|LSI|RP|LDA>        vector space method to represent the items [default: LSI]
    --k=<integer>                      number of topics for LSI, RP and LDA [default: 100]
    --N=<integer>                      number of recommendations [default: 5]

EXAMPLE:
========
$ python generate.py --input=example.json --output=out.json --debug
{'--N': '5',
 '--debug': True,
 '--display': False,
 '--extract': 'All',
 '--help': False,
 '--input': 'example.json',
 '--k': '100',
 '--method': 'LSI',
 '--output': 'out.json',
 '--preprocess': False,
 '--version': False}
[+] Loading items:
    -> Extracting text................................[OK]
[+] Creating the vector space:
    -> Computing the dictionary.......................[OK]
    -> Creating the bag-of-words space................[OK]
    -> Creating the LSI space.........................[OK]
[+] Generating recommendations........................[OK]
[+] Saving to output file.............................[OK]
[x] Finished.

$ python generate.py --input=example.json --output=out.json --debug --preprocess --N=10 --extract=title,description
{'--N': '10',                                                                                                                           
 '--debug': True,                                                                                                                       
 '--display': False,                                                                                                                    
 '--extract': 'title,description',                                                                                                      
 '--help': False,                                                                                                                       
 '--input': 'example.json',                                                                                                             
 '--k': '100',                                                                                                                          
 '--method': 'LSI',                                                                                                                     
 '--output': 'out.json',                                                                                                                
 '--preprocess': True,                                                                                                                  
 '--version': False}                                                                                                                    
[+] Loading items:                                                                                                                      
    -> Extracting text................................[OK]                                                                              
    -> Preprocessing text.............................[OK]
[+] Creating the vector space:
    -> Computing the dictionary.......................[OK]
    -> Creating the bag-of-words space................[OK]
    -> Creating the LSI space.........................[OK]
[+] Generating recommendations........................[OK]
[+] Saving to output file.............................[OK]
[x] Finished.


DEPENDENCIES:
============
1) Install python: http://www.python.org/getit/
2) Install pip: http://www.pip-installer.org/en/latest/installing.html
3) Then:
$ pip install docopt
$ pip install json
$ pip install pyyaml
$ pip install numpy
$ pip install scipy
$ pip install gensim
$ pip install nltk
$ python
>>> import nltk
>>> nltk.download()

TROUBLESHOOTING:
================ 
Q: How can I use the library with items stored in other formats than JSON?
A: You have to convert your file to JSON.
Q: How can I use the library directly with an item hash?
A: Simply import the library in Python and initialize a generator object with 
   the item hash of your preference.
Q: Is there any attribute that is required to be present in the item metadata?
A: Yes the 'id' attribute is mandatory.

CONTACT:
========
Nikolaos Pappas 
Idiap Research Institute
Centre du Parc, 
CH 1920 Martigny, 
Switzerland
E-mail:  nikolaos.pappas@idiap.ch 
Website: http://people.idiap.ch/npappas/ 


---
Last update:
16 Dec, 2013
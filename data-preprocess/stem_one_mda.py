# this script is for porter stemming one cleaned mda file (only have lower case english word)
# python is slow in I/O
# if wanna save module importing time, maybe use shell in python?

from nltk.stem.porter import *
import sys

content = sys.stdin.read() # eat the lines from command line 
stemmer = PorterStemmer() # the proter stemmer from nltk

# the content is seperate by blank
stemmed_list = []
for word in content.split():
    
    stemmed_word = stemmer.stem(word)
    stemmed_list.append(stemmed_word)

stemmed_text = " ".join(stemmed_list)

print(stemmed_text)


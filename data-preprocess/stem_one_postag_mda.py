# this script is for porter stemming one postag mda file

from nltk.stem.porter import *
import sys

lines = sys.stdin.read() # eat the file from command line 
stemmer = PorterStemmer() # the proter stemmer from nltk

content_list = lines.split()

stemmed_list = []
for postag_word in content_list:
    
    word = postag_word.split('_')[0]
    postag = postag_word.split('_')[1]
    stemmed_word = stemmer.stem(word)
    postag_stem_word = stemmed_word + '_' + postag[:2]  # now PR stands for PRP
    stemmed_list.append(postag_stem_word)

stemmed_text = " ".join(stemmed_list)

print(stemmed_text)

######### list of POStag #############
# CC
# CD
# DT
# EX
# FW
# IN
# JJ
# JJR
# JJS
# LS
# MD
# NN
# NNP
# NNS
# PDT
# PRP
# PRP$
# RB
# RBR
# RBS
# RP
# SYM
# TO
# VB
# VBD
# VBG
# VBN
# VBP
# VBZ
# WDT
# WP
# WP$
# WRB
########## end of list ########################

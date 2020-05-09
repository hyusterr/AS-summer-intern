# This script is to compute tfidf over all stem_mda files we have
# output a all.tfidf file, each row in the file is: filename wordID1:tfidf-score wordID2:tfidf-score
# input /tmp2/pcchien/intern/10k/*.postag_stem_mda , 10k/*.stem_mda output 1. tfidf files: test_tfidf.tfidf 2. word ID dictionary: test_tfidf.word.txt
# ignore 3, now we use ls | py to run the code due to long-argv limit.
# build a word ID dictionary first
# then use word ID as word expression
# run in home/intern/yushuang/sec/sec2.0
# can use re in bash directly

import os
import sys
import numpy as np
from collections import defaultdict

# path = '/tmp2/pcchien/intern/10k/' # all files store under it
# set a if-else condition for file_list

# === PC modify === #
file_list = [i.strip() for i in sys.stdin.readlines()] if len(sys.argv) == 1 else argv[1:] # .split('\n')[0].split()  # the final file contains \\n, that's weird

# we can use echo for path/* if the argv is too long

dir_name = file_list[1].split('.')[1]
path = "/".join(file_list[1].split('/')[:-1])

print( 'the files locate at ' + path )
print( 'now we are dealing with ' + dir_name + ' files.' )

dictionary = dir_name +  '-words.txt'
final_file = dir_name + '.tfidf'

# show information

print('the word ID form will be ' + dictionary)
print('the TFIDF file will be ' + final_file)
print('total files: ' + str(len(file_list)))

# build word ID dictionary

os.system('find ' + path + ' -wholename  "*.' + dir_name + '" -type f '  + '| xargs cat  | tr " " "\n" | sort | uniq | grep -v ^$ | cat -n > ' + dictionary) 

# find /tmp2/pcchien/intern/10k -wholename *.txt -type f | xargs cat
# build word ID dictionary

# bulid python dictionary for word_ID

with open(dictionary, 'r') as word_ID_file:
    # === PC modify === #

    #word_ID_file_content = word_ID_file.readlines()

    word_ID_dict = dict(map(lambda x: (x.split()[1], int(x.split()[0]), word_ID_file.readlines()))

    #word_ID_dict = {}

    # get the word id dictionary

    #for word_ID in word_ID_file_content:
       
        # ID, word = int(word_ID.split()[0]), word_ID.split()[1]
        #word_ID_dict[word_ID.split()[1]] = int(word_ID.split()[0])

print( 'successfully build word_ID_dict!' )
# keys are word in word_ID_dict

# calculate idf for each word, save in a idf_dict

idf_dict = {} # keys are wordID in idf_dict
total_num_of_documents = len(file_list)

word_occurence_dict = { a_word : 0 for a_word in word_ID_dict }    
# keys are word in word occurence dictionary

for doc in file_list:
    
    # === PC modify === #
    with open(doc) as f:
        for a_word in set( f.read().split() ):  
            word_occurence_dict[ a_word ] += 1
    #f = open(doc, 'r')
    #for a_word in set( f.read().split() ):  
    #    word_occurence_dict[ a_word ] += 1
    #f.close()

# === PC modify === #
idf_dict = {word_ID_dict[i]: np.log(total_num_of_documents / word_occurence_dict[i] for i in word_occurence_dict}
#for a_word in word_occurence_dict:
#    idf_dict[ word_ID_dict[ a_word ] ] =  np.log( float( total_num_of_documents ) / float( word_occurence_dict[ a_word ] ) )

print( 'sucessfully build idf_dict!' )

# calculate every word's tfidf in each document, match the format" filename wordID1:tfidf-score wordID2:tfidf-score (sort by wordID) ..."
all_tfidf = ''

for doc in file_list:

    f = open(doc, 'r')
    words_list = f.read().split()
    total_num_of_word_in_f = float(len(words_list))
    
    # === PC modify === #
    word_counts_dict = defaultdict(int)
    #word_counts_dict = {}
    filename = doc.split('/')[-1]
    
    for a_word in words_list:
        # === PC modify === #
        word_counts_dict[word_ID_dict[a_word]] += 1
        #if word_ID_dict[a_word] in word_counts_dict:
        #    word_counts_dict[word_ID_dict[a_word]] += 1
        #else:
        #    word_counts_dict[word_ID_dict[a_word]] = 1
    
    # === PC modify === #
    words_tfidf_list = sorted([(i, word_counts_dict[i] / total_num_of_word_in_f * idf_dict[i]) for i in word_counts_dict])
    #words_tfidf_list = []
   
    #for counted_word in word_counts_dict:
    #    
    #    word_counts_dict[counted_word] = float(word_counts_dict[counted_word]) / float( total_num_of_word_in_f) #get tf
    #    
    #    word_tfidf = word_counts_dict[counted_word] * idf_dict[counted_word] # get tf-idf, type=float
    #    words_tfidf_list.append((counted_word, word_tfidf))

    # === PC modify === #

    #words_tfidf_list_sort = sorted(words_tfidf_list)
    #tfidf_info_list = []
    #for word_tfidf_tuple in words_tfidf_list_sort:
    #    format_word = ":".join('%d:%f' % inst for inst in word_tfidf_tuple) # format it
    #    tfidf_info_list.append(format_word)
    tfidf_info_list = ['%d:%f' % word for word in words_tfidf_list]

    write_to_all_tfidf = filename + ' ' + " ".join(tfidf_info_list) + '\n' # a row represent a mda_file
    

    all_tfidf += write_to_all_tfidf 
    f.close()

    print( filename + ' is added to ' + final_file + '!' )

# write it to all.tfidf file
with open(final_file, 'w') as new_file:
    new_file.write(all_tfidf)
    new_file.close()

# -*- coding: utf-8 -*-

# this script is for connect tfidf file to integar part of z-score of financial index
# usage python atv.py trading_vol_data query_data | python z.py | python connect.py tfidf_data

import sys

# firm_index<TAB>yyyymmdd word_id:tfidf ...
with open( sys.argv[1], 'r' ) as f:
    tfidf_dict = { "\t".join( l.strip().split()[:2] ): " ".join( l.strip().split()[2:] ) for l in f.readlines() }

for d in sys.stdin.readlines():
    if '\t'.join( d.strip().split()[:2] ) in tfidf_dict and tfidf_dict[ "\t".join( d.strip().split()[:2] ) ] != "":
        print( d.strip().split()[2] + ' ' + 'qid:' + d.strip().split()[1][:-4] + ' ' + tfidf_dict[ "\t".join( d.strip().split()[:2] ) ] )

# PC會幫我把 ~~.stem_mda  改成 firm_index<TAB>yyyymmdd<TAB>
# python split() TAB = blank space
# qid 留日期前四碼就可(年) firm_index<TAB>yyyy
# z 限制在 [-2, 2]

#z_list = []

#for d in data:
#    z_list.append( float( d[2] ) )

#z_list = stats.zscore( np.array( z_list ) )
#
#for i in range( len( data ) ):
#    data[i][2] = str( int( z_list[i] ) )
#    print( "\t".join( data[i] ) )


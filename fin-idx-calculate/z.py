# this script is for calculating z-score for the output

import sys
import numpy as np
from scipy import stats

data = [ d.split() for d in sys.stdin.readlines() ] # list of string for each row

z_list = []

for d in data:
    z_list.append( float( d[2] ) )

z_list = stats.zscore( np.array( z_list ) )

for i in range( len( data ) ):

    if int( z_list[i] ) > 2:
        data[i][2] = str( 2 )

    elif int( int( z_list[i] ) ) < -2:
        data[i][2] = str( -2 )

    else:
        data[i][2] = str( int( z_list[i] ) )

    print( "\t".join( data[i] ) )

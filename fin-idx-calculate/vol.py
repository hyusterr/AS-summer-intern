# this script is for calculating volatility

import sys
from datetime import *
import numpy as np

# np.seterr( divide = 'ignore' )

stock_price_filename = sys.argv[1]
query_filename       = sys.argv[2]

# build dictionary contains stock price data, key: date and company

stock_dict = {}

with open( stock_price_filename, 'r' ) as f:
# date here is actually a string
    for s in f.readlines()[1:]:
        try:
            stock_dict[( s.strip().split()[1], datetime.strptime( s.strip().split()[0] , '%Y/%m/%d' ) )] =  float( s.strip().split()[2] )
        except:
            pass
    f.close()

# read query as a list

with open( query_filename, 'r' ) as query_file:
    query_list = [ ( query.split()[0], datetime.strptime( query.split()[1], '%Y/%m/%d' ) ) for query in query_file.readlines() ] # (firm_index, date: yyyy/mm/dd)
    query_file.close()


# Ri = Si/S(i-1) - 1
# R_bar = sum( Ri ) / n + 1 over [ t-n, t ]
# v = ( sum( (Ri - R_bar)**2 ) / n )**0.5
# N = 12month after release


def daterange(start_date, end_date):
    for n in range( int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def volatility( query ):

    firm = query[0]
    zero = query[1]
    returns = []

    for t in daterange( zero, zero + timedelta( days=366 ) ): # in one year, is there gonna be only 252?
        
        if ( firm, t ) in stock_dict:
            returns.append( stock_dict[ firm, t ] ) # there should be n + 1 Ri
    
    if len( returns ) > 200:
        v = np.std( np.array( returns ) )
        if v != None and str( v ) != 'nan': 
            print( query[0] + '\t' + query[1].strftime( '%Y%m%d' ) + '\t' + str( v ) )

for q in query_list:
    volatility( q )

# this script is for calculating excess return

import sys
from datetime import *

# eat argv

sp500_filename       = sys.argv[1]
stock_price_filename = sys.argv[2]
query_filename       = sys.argv[3]

# print( 'build sp500 dictioary...' )
# read S&P500 file
sp500_dict = {}

with open( sp500_filename, 'r' ) as f:
    for sp in f.readlines()[1:]:
        if len( sp.strip().split() ) == 2:
            sp500_dict[ datetime.strptime( sp.strip().split()[ 0 ], '%Y/%m/%d' ) ] = float( sp.strip().split()[ 1 ] ) 
    f.close()

# build sp500 dictionary
# read company stock price as a order dictionary
# question: will nested dictionary be faster?
stock_dict = {}

# print( 'Build stock price dictionary...' )

with open( stock_price_filename, 'r' ) as f:
    for st in f.readlines()[1:]:
        if len( st.strip().split() ) == 3:
            stock_dict[ ( st.strip().split()[ 1 ],  datetime.strptime( st.strip().split()[ 0 ], '%Y/%m/%d' ) )] =  float( st.strip().split()[ -1 ] )
    f.close()

# read query file as a list

# print( 'Build query dictioanry' )

with open( query_filename, 'r' ) as f:
    query_list = [ ( q.strip().split()[0], datetime.strptime( q.strip().split()[1], '%Y/%m/%d' ) )  for q in f.readlines() ]
    f.close() 

# set formula, (date, company) in a query
# window = [0, 3]

def excess_return( query ):
    
    firm = query[0]
    zero_date = query[1]

    if query in stock_dict and zero_date in sp500_dict: 
        stock_zero_date_price  = stock_dict[ query ]
        sp500_zero_date_price  = sp500_dict[ zero_date ]
       
        if ( firm, zero_date + timedelta( days=3 ) ) in stock_dict: # if zero day is Mon, Tue
            stock_third_date_price = stock_dict[ ( firm, zero_date + timedelta( days=3 ) ) ]
            sp500_third_date_price = sp500_dict[ zero_date + timedelta( days=3 ) ]
            #print( zero_date )
            #print( zero_date + timedelta( days=3 ) )

        elif ( firm, zero_date + timedelta( days=5 ) ) in stock_dict: # if zero day is Wes, Thu, Fri
            stock_third_date_price = stock_dict[ ( firm, zero_date + timedelta( days=5 ) ) ]
            sp500_third_date_price = sp500_dict[ zero_date + timedelta( days=5 ) ]
            #print( zero_date )
            #print( zero_date + timedelta( days=5 ) )

        else: # if three days after the release day is not exist
            pass

    else: # if the query is not even in the stock dictionary
        pass
    
    try:
        stock_return = ( stock_third_date_price - stock_zero_date_price ) / stock_zero_date_price
        sp500_return = ( sp500_third_date_price - sp500_zero_date_price ) / sp500_zero_date_price
        excess_return = stock_return - sp500_return
    
        return firm + '\t' + zero_date.strftime( '%Y%m%d' ) + '\t' + str( excess_return )
    
    except NameError:
        pass
        
for q in query_list:
    if excess_return( q ) != None:
        print( excess_return( q ) )

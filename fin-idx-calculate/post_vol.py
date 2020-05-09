# this script is for calculating post-event volatility

# import module

import sys
from datetime import *
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

# eat argv

fama_french_file = sys.argv[1] # yyyy/mm/dd<TAB>Rf<TAB>Rm-Rf<TAB>SMB<TAB>HML
return_file      = sys.argv[2] # yyyy/mm/dd<TAB>firm_index<TAB>return_rate
query_file       = sys.argv[3] # firm_index<TAB>yyyy/mm/dd

# build fama french ordereddict 

ff_odict = {}

with open( fama_french_file, 'r') as f: # key is date
    for ff in f.read().strip().splitlines()[2:]:
        if len( ff.strip().split() ) == 5:
            ff_odict[ datetime.strptime( ff.strip().split()[0], '%Y/%m/%d' )] = [ float( ff.strip().split()[1] ) , float( ff.strip().split()[2] ),  float( ff.strip().split()[3] ), float(ff.strip().split()[4] ) ]
    f.close()

# build return ordereddict

rr_odict = {}
with open( return_file, 'r' ) as f: # key is firm, date
    
    for rr in f.readlines()[1:]:
        try: 
            rr_odict[ ( rr.split()[1], datetime.strptime( rr.split()[0], '%Y/%m/%d' ) )] = float( rr.strip().split()[2] )
        except ValueError:
            pass
    f.close()

# build query list

with open( query_file, 'r' ) as f: # key is firm, date
    q_list = [ ( q.strip().split()[0], datetime.strptime( q.strip().split()[1], '%Y/%m/%d' ) ) for q in f.readlines() ]
    f.close()


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

# build pev formula

def post_event_volatility( query ):

    firm     = query[0]
    rel_date = query[1]
    # zero_ff  = ff_odict.keys().index( rel_date ) # for the day 10K was released, get its index in ff_odict
    # zero_rr  = rr_odict.keys().index( query )    # what if not exist?

    # regression's input

    X  = []
    y  = []

    for i in range( 6, 366 ):
        
        # judge if ff exist at that day and rr for the firm exist at that day, if exist then append

        if ( firm, rel_date + timedelta( days=i ) ) in rr_odict and rel_date + timedelta( days=i ) in ff_odict and len( y ) < 252:

            X.append( ff_odict[ rel_date + timedelta( days=i ) ] )  # list contain ff information
            y.append( rr_odict[ firm, rel_date + timedelta( days=i ) ] ) # rr's value

    # print( y )
    # print( X )
    y = np.array( y )
    X = np.array( X )
    
    if len( y ) >= 60:

        lr     = LinearRegression().fit( X, y )
        y_pred = lr.predict( X )
        pev    = float( ( mean_squared_error( y, y_pred ) ) ** 0.5 )
        # print( y_pred )
        return ( q[0] + '\t' + q[1].strftime( '%Y%m%d' ) + '\t' + str( pev ) )

    else:

        pass
            
# output

for q in q_list:
    if post_event_volatility( q ) != None:
        print( post_event_volatility( q ) )

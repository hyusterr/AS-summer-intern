#!/usr/bin/python
# -*- coding: utf-8 -*-

# this script is for calculate abnormal trading volume

import sys
from datetime import *
import numpy as np

trad_vol_filename = sys.argv[1]
query_filename = sys.argv[2]

# build dictionary contains trading value data, key: date and company

with open( trad_vol_filename, 'r' ) as f:
    trad_dict = {}
    for trad in f.readlines()[1:]:
        if len( trad.split() ) == 3:
            trad_dict[ ( trad.split()[1], datetime.strptime( trad.split()[0], '%Y/%m/%d' ) ) ] = float( trad.split()[2] )
    f.close()

# read query as a list

with open( query_filename, 'r' ) as f:
    query_list = [ ( q.strip().split()[0], datetime.strptime( q.strip().split()[1], '%Y/%m/%d' ) ) for q in f.readlines() ]
    # (firm_index, date)
    f.close()

# the abnormal trading volume is defined as the average volume of the 4d event
# window [0, 3], in which volume is standardized based on its mean and standard
# deviation from days [−65, −6] of the so-called pre-event window.

def daterange(start_date, end_date):

    for n in range( int( ( end_date - start_date ).days ) ):
         yield start_date + timedelta( n )

def abnormal_vol( query ): # input tuple( firm_index_string, datetime_obj )
    
    release_date  = query[1]  
    firm          = query[0]
    
    history = []
    future  = []
    
    i = -6
    while len( history ) < 60 and i > -120:
        
        if ( firm, release_date + timedelta( days=i ) ) in trad_dict:
            history.append( trad_dict[ firm, release_date + timedelta( days=i ) ] )
        i -= 1

    j = 0
    while len( future ) < 4 and j < 10:
        if ( firm, release_date + timedelta( days=j ) ) in trad_dict:
            future.append( trad_dict[ firm, release_date + timedelta( days=j ) ] )
        j += 1
    
    mean     = np.mean( np.array( history ) ) if len( history ) == 60 else None
    std      = np.std ( np.array( history ) ) if len( history ) == 60 else None
    average  = np.mean( np.array( future  ) ) if len( future  ) == 4  else None
    
    try:
        atv = ( average - mean ) / std
        return str( atv )
    
    except TypeError:
        pass

# problem: what if volume data not exist or the next value is belong to another company?

for q in query_list:
    if abnormal_vol( q ) != None:
        print( q[0] + '\t' + q[1].strftime( '%Y%m%d' ) + '\t' + abnormal_vol( q ) )

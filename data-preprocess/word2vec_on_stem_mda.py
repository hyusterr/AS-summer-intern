# this script is for build word2vec model on all stem_mda and postag_stem_mda model
# use echo /tmp2/pcchien/intern/10k/*.stem_mda

from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys

##########################################################################################
# train w2v model, footnote as training ended
#
#file_list = sys.stdin.read().split() 
#corpus_list = []
#
#corpus_type = file_list[ 0 ].split( '/' )[ -1 ].split( '.' )[ -1 ]
#
#for name in file_list:
#    with open( name, 'r' ) as f:
#        corpus_list.append( f.read().split() )
#
#path = get_tmpfile( corpus_type + '_w2v.model' )
#
#model = Word2Vec(corpus_list, size=200, window=5, min_count=100, workers=4)
#
#model.save( corpus_type + '_w2v.model' )
#
#print( 'w2v model is built' )
##########################################################################################

corpus_type = 'stem_mda'
model = Word2Vec.load( "stem_mda_w2v.model" )

def tsne_plot( model ):
    labels = []
    tokens = []

    for word in model.wv.vocab:
        tokens.append( model[ word ] )
        labels.append( word )

    tsne_model = TSNE( perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23 )
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])
                                                                                            
    plt.figure(figsize=(16, 16)) 

    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
        plt.show()
        plt.savefig( corpus_type + 'w2v_vis.png' )

tsne_plot(model)
        

# this script is for apply extract MDA >>>only keep lower case English >>> postag >>> stem >>>tfidf
# postagger can only eat input from file, sad

for form10k in /tmp2/pcchien/intern/10k/*.txt
do
	perl extract_MDA.pl $form10k | tee ${form10k/txt/mda} |
		tr [:upper:] [:lower:] | tr -cd [a-z][:space:] | tee ${form10k/txt/cleaned_mda} |
			python stem_one_mda.py > ${form10k/txt/stem_mda}

  ./stanford-postagger.sh models/wsj-0-18-left3words-distsim.tagger ${form10k/txt/cleaned_mda} |
		python stem_one_postag_mda.py > ${form10k/txt/postag_stem_mda}
done

# apply tfidf
echo /tmp2/pcchien/intern/10k/*.stem_mda | python tfidf.py
echo /tmp2/pcchien/intern/10k/*.postag_stem_mda | python tfidf.py

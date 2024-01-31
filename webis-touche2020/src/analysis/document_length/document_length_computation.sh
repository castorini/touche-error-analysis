dataset=webis-touche2020
echo $dataset
python corpus_length_analysis.py $dataset green 95 1000000

dataset=hotpotqa
echo $dataset
python corpus_length_analysis.py $dataset red 99 1000000

dataset=msmarco
echo $dataset
python corpus_length_analysis.py $dataset blue 99 1000000
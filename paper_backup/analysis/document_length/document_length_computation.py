import matplotlib.pyplot as plt
from beir import LoggingHandler
from beir.datasets.data_loader import GenericDataLoader
from nltk import word_tokenize

import logging
import pathlib, os
import string
import tqdm
import numpy as np
import argparse

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
#### /print debug information to stdout


#make translator object
translator=str.maketrans('','',string.punctuation)

argparser = argparse.ArgumentParser()
argparser.add_argument('--dataset', type=str, default='webis-touche2020')
argparser.add_argument('--color', type=str, default='#0504aa')
argparser.add_argument('--percentile_max', type=int, default=99)
argparser.add_argument('--y_lim', type=int, default=None)
argparser.add_argument('--data_dir', type=str, default="/store2/scratch/n3thakur/beir-datasets/")
args = argparser.parse_args()

logging.info(f"Dataset: {args.dataset}")
data_path = f"{args.data_dir}/{args.dataset}"

#### Provide the data_path where webis-touche2020 has been downloaded and unzipped
corpus, queries, qrels = GenericDataLoader(data_folder=data_path).load(split="test")

passage_lengths = []
for key, value in tqdm.tqdm(corpus.items(), total=len(corpus)):
    paragraph = corpus[key]["text"]
    title = corpus[key]['title']
    text = title + " " + paragraph
    text = text.translate(translator)
    passage_lengths.append(len(word_tokenize(text)))

# An "interface" to matplotlib.axes.Axes.hist() method
x = np.array(passage_lengths)
q25, q75 = np.percentile(x, [25, 75])
bin_width = 2 * (q75 - q25) * len(x) ** (-1/3)
x_max = np.percentile(x, [args.percentile_max])[0]
x_new = np.array([plen for plen in passage_lengths if plen <= x_max])
bins = round((x_max - 0) / bin_width)
logging.info(f"Freedman–Diaconis number of bins: {bins}")

# Plot the histogram.
plt.hist(x_new, density=False, bins=bins, rwidth=0.9, color=args.color, alpha=0.9)
plt.yscale('log')

# if y lim is provided, set it
if args.y_lim:
    plt.ylim(1, args.y_lim)

# Set the title and labels
plt.ylabel("", fontsize=18)
plt.xticks(fontsize=25, rotation=45)
plt.yticks(fontsize=25)
plt.xlabel(f"", fontsize=18)
plt.title("")

# If you want to save the plot locally, uncomment the below line
if args.y_lim:
    plt.savefig(os.path.join(
        pathlib.Path(__file__).parent.absolute(), "output", 
        f"{args.dataset}-corpus-{args.color}-{args.percentile_max}-ylim-{args.y_lim}.pdf"), bbox_inches="tight"
        );

# If you want to save the plot locally, uncomment the below line
plt.savefig(os.path.join(
    pathlib.Path(__file__).parent.absolute(), "output", 
    f"{args.dataset}-corpus-{args.color}-{args.percentile_max}.pdf"), bbox_inches="tight"
    );
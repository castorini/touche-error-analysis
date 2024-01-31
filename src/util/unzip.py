import zipfile

with zipfile.ZipFile('/store2/scratch/n3thakur/beir-datasets/webis-touche2020/webis-touche2020.zip', 'r') as zip_ref:
    zip_ref.extractall('/store2/scratch/n3thakur/beir-datasets/final/')
#!/bin/bash

# notice: modify load tsv meta files in seamless_communication/datasets/huggingface.py
m4t_prepare_dataset --source_lang eng --target_lang yue --split train --save_dir /home/do/ssd/data/m4t-traindata
m4t_prepare_dataset --source_lang eng --target_lang yue --split validation --save_dir /home/do/ssd/data/m4t-traindata

python3 truncate-fleurs-corpus.py /home/do/ssd/data/m4t-traindata/train_manifest.json 2030 
python3 truncate-fleurs-corpus.py /home/do/ssd/data/m4t-traindata/validation_manifest.json 2030 

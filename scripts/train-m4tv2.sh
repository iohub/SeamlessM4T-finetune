#!/bin/bash

DATASET_DIR=/home/do/ssd/data/m4t-traindata

m4t_finetune \
   --mode TEXT_TO_SPEECH \
   --train_dataset $DATASET_DIR/train_manifest.json  \
   --eval_dataset $DATASET_DIR/validation_manifest.json \
   --learning_rate 1e-6 \
   --warmup_steps 100 \
   --max_epochs 10 \
   --patience 5 \
   --model_name seamlessM4T_v2_large \
   --save_model_to $DATASET_DIR/checkpoint.pt

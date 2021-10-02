# train_targetID

Repository for training target ID system on AUVSI SUAS targets.

## Installation

This repository requires tensorflow and tflite. 

## Training

This repository uses tflite-model-maker to create the object detectors. 

For documentation of that API, see here: https://www.tensorflow.org/lite/api_docs/python/tflite_model_maker/object_detector

Currently, only efficientdet models are supported by Model Maker. I'm not fully satisfied with the model-maker API (you cannot stop and continue training from a `.ckpt`, for example, and a lot of customizations to the model are unclear.)

Training is done with the jupyter notebook `train.ipynb` in this directory. Run

```jupyter notebook```

and navigate to it to run training.

## Datasets

You need `.tfrecord` files created by the generator to train. To get those, you can generate them (see the `data_gen` folder) or you can download pre-generated ones. If you are on UCI UAV Forge, those will be made available on the drive shortly. If you are using this repository from outside UCI, send me an email and I can send you those datasets. Unless you're on a team that is competing with us, then... I'll probably still send them :-)

## Contact

For questions, e-mail Mike at msutherl@uci.edu.
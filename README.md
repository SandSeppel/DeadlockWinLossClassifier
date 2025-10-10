# Collection of classifier models which predict lane outcomes based on heroes for Deadlock
Due to many missing factors and only having hero picks as information for predicting, the accuracy is obviously not nearly reliable, but tends to be better with higher ranks, probably due to high rank players playing less randomly and more deterministic. Most models predicting eternus lobbies can reach an accuracy of almost 70%, while practically guessing in initiate.

## Quick Start

#### Install requirements
```bash
pip install -r requirements.txt
```
Note that you still have to install pytorch manually due to the installation being dependent on your system specs.
https://pytorch.org/get-started/locally/

#### Usage
Download a pretrained model you want to use over at the release tab or train your own model with loop.py
Edit the `config.cfg` file to path to your saved model

Run `run.py`, and thats it!

## Future of this project
I will definately continue to tinker around with this project and add more information to feed into the model to get more accurate predictions of the game, feel free to contribute or add suggestions!

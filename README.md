# Music Composition with Machine Learning

[Download Generated MIDI File](generated.mid)

## Overview

This project demonstrates a simple approach to music composition using machine learning. An LSTM model is trained on synthetic musical sequences to learn note patterns and generate new music. The generated sequence is then converted into a MIDI file, which you can listen to using any MIDI player.

This repository includes both a Jupyter Notebook (`Music_Composition_with_Machine_Learning.ipynb`) and a Python script (`music_composition_with_machine_learning.py`) that implement the complete music composition pipeline.

## Repository Contents

- **generated.mid**: A sample generated MIDI file.
- **Music_Composition_with_Machine_Learning.ipynb**: Jupyter Notebook containing the complete implementation.
- **music_composition_with_machine_learning.py**: Python script version of the project.
- **README.md**: This file.

## Features

- **LSTM-Based Music Generation**: Uses a Long Short-Term Memory (LSTM) network to learn and generate musical sequences.
- **Synthetic Dataset**: Generates synthetic sequences to mimic musical phrases.
- **MIDI Conversion**: Converts generated note sequences into a MIDI file using the `pretty_midi` library.
- **Google Colab Compatibility**: Designed to run on Google Colab for ease of experimentation and demonstration.

## Requirements

- Python 3.x
- [TensorFlow](https://www.tensorflow.org/)
- [pretty_midi](https://github.com/craffel/pretty-midi)
- NumPy

You can install the required packages using pip:

```bash
pip install tensorflow pretty_midi numpy
```

## Running the Project

### On Google Colab

1. Open the `Music_Composition_with_Machine_Learning.ipynb` notebook in Google Colab.
2. Run the cells sequentially. The notebook installs dependencies, trains the model, and generates a MIDI file named `generated.mid`.
3. Once the notebook finishes, you can download the `generated.mid` file from the file explorer in Colab.

### Locally

1. Clone the repository:

```bash
git clone https://github.com/mohiuddin-khan-shiam/Music-Composition-with-Machine-Learning.git
cd Music-Composition-with-Machine-Learning
```

2. Install the required dependencies:

```bash
pip install tensorflow pretty_midi numpy
```

3. Run the Python script:

```bash
python music_composition_with_machine_learning.py
```

The script will generate a MIDI file named `generated.mid` in the repository directory.

## How It Works

### Data Generation

The project generates synthetic musical sequences using a random walk approach within a defined MIDI note range. These sequences serve as training data for the model.

### Model Training

An LSTM network is built with an embedding layer, an LSTM layer, and a dense output layer. The model is trained to predict the next note in the sequence using the synthetic dataset.

### Music Generation

Using a seed sequence from the training data, the model generates new musical notes. Temperature sampling is applied to control the randomness of the predictions.

### MIDI File Creation

The generated sequence of notes is converted into a MIDI file using the `pretty_midi` library. Each note is assigned a fixed duration to create a continuous musical piece.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgements

- Thanks to the developers of TensorFlow and pretty_midi for providing the tools needed for machine learning-based music composition.
- Inspiration from various music generation projects and research papers in the field of deep learning and music.

Feel free to modify any sections as needed to better match your project's details or preferences. Enjoy sharing your machine learning music composition project!


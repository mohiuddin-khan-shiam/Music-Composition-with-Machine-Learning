# -*- coding: utf-8 -*-
"""Music Composition with Machine Learning.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FLf_3UMn3viJdu07RxEPS1qC-VIku4tI
"""

# Install required package (run this cell once)
!pip install pretty_midi

# Import required modules
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
import pretty_midi
import os
from IPython.display import Audio, display

# ----- Step 1: Generate Synthetic Music Dataset -----

# Define the MIDI note range (for example, notes from Middle C (60) to C above (72))
vocab_start = 60
vocab_end = 72
vocab_size = vocab_end - vocab_start + 1  # e.g., 13 possible notes

num_sequences = 1000          # Number of sequences to generate
sequence_total_length = 50    # Total length of each generated sequence
input_sequence_length = 20    # Length of input sequences for training

# Generate synthetic sequences using a random walk so that adjacent notes are related.
sequences = []
for _ in range(num_sequences):
    seq = []
    # Start at a random note in the range
    note = np.random.randint(vocab_start, vocab_end + 1)
    seq.append(note)
    for _ in range(1, sequence_total_length):
        # Random step between -2 and +2 semitones
        step = np.random.choice([-2, -1, 0, 1, 2])
        note = note + step
        # Ensure the note stays within our defined range
        note = int(np.clip(note, vocab_start, vocab_end))
        seq.append(note)
    sequences.append(seq)

# Create training examples by sliding over each sequence:
X = []
y = []
for seq in sequences:
    # Convert note values to indices (0 to vocab_size-1)
    seq_indices = [note - vocab_start for note in seq]
    for i in range(len(seq_indices) - input_sequence_length):
        X.append(seq_indices[i:i+input_sequence_length])
        y.append(seq_indices[i+input_sequence_length])
X = np.array(X)
y = np.array(y)

print("Training examples:", X.shape, y.shape)

# ----- Step 2: Build and Train the LSTM Model -----

embedding_dim = 64
lstm_units = 128

model = Sequential([
    # The Embedding layer converts integer indices to dense vectors.
    Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=input_sequence_length),
    LSTM(lstm_units),
    Dense(vocab_size, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam')
model.summary()

# Train the model (adjust epochs as needed; training on a synthetic dataset is fast)
epochs = 50
batch_size = 64
model.fit(X, y, epochs=epochs, batch_size=batch_size)

# ----- Step 3: Generate New Music -----

def generate_music(seed_seq, gen_length=100, temperature=1.0):
    """
    Generates a new sequence of note indices.
    - seed_seq: a list of integers (length should equal input_sequence_length)
    - gen_length: number of notes to generate
    - temperature: controls randomness (higher => more random)
    """
    generated = seed_seq.copy()
    for _ in range(gen_length):
        # Prepare the input sequence (reshape to (1, sequence_length))
        input_seq = np.array(generated[-input_sequence_length:]).reshape(1, input_sequence_length)
        predictions = model.predict(input_seq, verbose=0)[0]
        # Apply temperature scaling
        predictions = np.log(predictions + 1e-8) / temperature
        exp_preds = np.exp(predictions)
        predictions = exp_preds / np.sum(exp_preds)
        # Sample the next note index from the probability distribution
        next_index = np.random.choice(range(vocab_size), p=predictions)
        generated.append(next_index)
    return generated

# Choose a random seed from the training set
seed_index = np.random.randint(0, len(X))
seed_sequence = list(X[seed_index])
print("Seed sequence (indices):", seed_sequence)

generated_sequence = generate_music(seed_sequence, gen_length=100, temperature=1.0)

# Convert indices back to MIDI note numbers
generated_notes = [n + vocab_start for n in generated_sequence]
print("Generated note sequence:", generated_notes)

# ----- Step 4: Convert Generated Notes to a MIDI File -----

def notes_to_midi(notes, output_file="generated.mid", note_duration=0.5, start_time=0.0):
    """
    Converts a list of MIDI note numbers into a MIDI file.
    - notes: list of MIDI note numbers (integers)
    - output_file: name/path for the output MIDI file
    - note_duration: duration (in seconds) for each note
    - start_time: starting time offset
    """
    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano
    current_time = start_time
    for note in notes:
        note_event = pretty_midi.Note(
            velocity=100,
            pitch=note,
            start=current_time,
            end=current_time + note_duration
        )
        instrument.notes.append(note_event)
        current_time += note_duration
    pm.instruments.append(instrument)
    pm.write(output_file)
    print(f"MIDI file saved as '{output_file}'")

# Convert the generated note sequence into a MIDI file
notes_to_midi(generated_notes, output_file="generated.mid")

# ----- (Optional) Listen to the MIDI File in Colab -----
# Note: Colab's Audio player may not render MIDI directly.
# For a better listening experience, you could convert the MIDI file to audio using a synthesizer.
# Below, we simply provide a link to the MIDI file.
if os.path.exists("generated.mid"):
    print("Generated MIDI file is available for download: 'generated.mid'")
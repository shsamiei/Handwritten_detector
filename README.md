# Handwritten Digit Recognition

This project implements a system to recognize handwritten digits using deep neural networks.
## Overview

  Developed a convolutional neural network model architecture for digit classification
    Used convolutional and pooling layers to extract visual features from digit images
    Added fully connected layers at the end for prediction
    Trained the model on the MNIST dataset of 60,000 handwritten digit images
    Achieved over 97% accuracy in recognizing unseen handwritten digits

## Model Architecture

  Initial convolutional layers detect low-level features like edges, strokes
    Max pooling layers reduce dimensions while keeping important details
    Increased number of filters in later convolutions to identify higher-level patterns
    Fully connected layers at the end for digit classification
    Output layer with 10 nodes to predict probability distribution over 10 digits

## Technical Implementation

  Built using TensorFlow and Keras deep learning frameworks
    Model training leverages GPU acceleration for faster iteration
    Python scripts to load MNIST dataset, train model, and evaluate accuracy
    Exports trained model to make predictions on new digit images, This handwriting recognition model serves as a good baseline for computer vision tasks. The project can be extended by using larger datasets, augmenting data, and experimenting with enhanced model architectures.

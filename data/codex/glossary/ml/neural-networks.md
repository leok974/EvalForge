---
title: Neural Networks
id: ml/neural-networks
---
# Neural Networks

Models inspired by biological neurons.

## Components
- **Input Layer**: Features
- **Hidden Layers**: Learn representations
- **Output Layer**: Predictions
- **Activation Functions**: ReLU, Sigmoid, Softmax

## Simple Example (Keras)
```python
from tensorflow import keras
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])
```

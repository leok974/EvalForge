## Outcome
You will learn how a basic training loop works (forward pass → loss → gradients → update) and how metrics help you tell whether learning is improving.

## Concept in 30 seconds
Training is iterative improvement. You start with parameters (weights), make predictions, measure how wrong you are using a **loss**, compute **gradients** (which direction reduces loss), and update weights using a **learning rate**. Metrics like loss over time tell you if training is actually working.

## Key terms
- **Loss**: A number measuring how wrong predictions are.
- **Gradient**: The direction to change weights to reduce loss.
- **Learning Rate**: How big each update step is.
- **Epoch**: One full pass through the training data.
- **Metric**: A tracked value that measures training progress.

## Walkthrough
1) Initialize weights (often zeros or small random values).
2) For each epoch:
   - predict outputs (forward pass)
   - compute loss
   - compute gradient of loss w.r.t. weights
   - update weights with learning rate
3) Track loss every epoch (or every few epochs).
4) Click **Run** to confirm loss decreases over epochs.
5) Use **Submit** when your loop updates weights correctly and metrics behave as expected.

## Example implementation
A tiny linear regression training loop using NumPy (no deep learning frameworks required):

```py
import numpy as np

# Toy data: y ≈ 2x + 1
x = np.array([0.0, 1.0, 2.0, 3.0])
y = np.array([1.0, 3.0, 5.0, 7.0])

w = 0.0
b = 0.0
lr = 0.1
epochs = 50

for epoch in range(epochs):
    y_hat = w * x + b
    error = y_hat - y
    loss = np.mean(error ** 2)

    # Gradients for MSE
    dw = 2 * np.mean(error * x)
    db = 2 * np.mean(error)

    # Update
    w -= lr * dw
    b -= lr * db

    if epoch % 10 == 0:
        print(f"epoch={epoch} loss={loss:.4f} w={w:.3f} b={b:.3f}")
```

## Common mistakes
- **Updating weights in the wrong direction** (using += instead of -=).
- **Learning rate too large** (loss explodes) or too small (loss barely changes).
- **Forgetting to average gradients** (scale becomes too large with bigger datasets).
- **Mixing up loss vs metric** (loss is a metric, but you may also track accuracy, etc.).
- **Printing every step** (hard to read); sample metrics periodically.

## Check yourself
- What role does the learning rate play?
- What does a gradient tell you?
- If loss increases every epoch, what are two likely causes?

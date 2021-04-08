import random
from neural_network import NeuralNetWork


data = [
    [1, [1, 0]],
    [1, [0, 1]],
    [0, [0, 0]],
    [0, [1, 1]]
]

brain = NeuralNetWork(2, 4, 1)

# training
for _ in range(10000):
    index = random.randrange(len(data))
    inputs = data[index][1]
    labels = [data[index][0]]
    brain.train(inputs, labels)

output = brain.predict([1, 0])
print(output)
output = brain.predict([0, 1])
print(output)
output = brain.predict([1, 1])
print(output)
output = brain.predict([0, 0])
print(output)

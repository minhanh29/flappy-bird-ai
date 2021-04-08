import numpy as np
from random import random, gauss


class NeuralNetWork():
    def __init__(self, i, h, o, mutate_rate=0.01, learning_rate=0.1):
        if isinstance(i, NeuralNetWork):
            self.w_ih = i.w_ih.copy()
            self.w_ho = i.w_ho.copy()

            self.bias_h = i.bias_h.copy()
            self.bias_o = i.bias_o.copy()
        else:
            self.w_ih = np.matrix(np.random.uniform(-1, 1, (h, i)))
            self.w_ho = np.matrix(np.random.uniform(-1, 1, (o, h)))

            self.bias_h = np.matrix(np.random.uniform(-1, 1, (h, 1)))
            self.bias_o = np.matrix(np.random.uniform(-1, 1, (o, 1)))

        self.learning_rate = learning_rate
        self.mutate_rate = mutate_rate

    def predict(self, inputs):
        if not isinstance(inputs, np.ndarray):
            input_matrix = np.matrix(inputs).transpose()

        # input to hidden layer
        # compute weighted sum and add bias
        hidden_matrix = self.w_ih * input_matrix + self.bias_h

        # apply activation function
        hidden_matrix = self.sigmoid(hidden_matrix)

        # hidden to output layer
        # compute weighted sum and add bias
        output_matrix = self.w_ho * hidden_matrix + self.bias_o

        # apply activation function
        output_matrix = self.sigmoid(output_matrix)

        return output_matrix.tolist()

    def train(self, inputs, labels):
        if isinstance(inputs, np.matrix):
            input_matrix = inputs
        else:
            input_matrix = np.matrix(inputs).transpose()

        # FEED FORWARD
        # input to hidden layer
        # compute weighted sum and add bias
        hidden_matrix = self.w_ih * input_matrix + self.bias_h

        # apply activation function
        hidden_matrix = self.sigmoid(hidden_matrix)

        # hidden to output layer
        # compute weighted sum and add bias
        output_matrix = self.w_ho * hidden_matrix + self.bias_o

        # apply activation function
        output_matrix = self.sigmoid(output_matrix)

        # COMPUTE ERRORS
        # convert label to matrix
        if isinstance(labels, np.matrix):
            label_matrix = labels
        else:
            label_matrix = np.matrix(labels).transpose()

        # the output error
        output_error = label_matrix - output_matrix

        # the hidden error
        hidden_error = self.w_ho.transpose() * output_error

        # COMPUTE DELTA
        # hidden to output delta
        output_matrix = self.desigmoid(output_matrix)
        bias_o_delta = np.multiply(output_error, output_matrix) *\
            self.learning_rate
        ho_delta = bias_o_delta * hidden_matrix.transpose()

        # similarly, input to hidden
        hidden_matrix = self.desigmoid(hidden_matrix)
        bias_h_delta = np.multiply(hidden_error, hidden_matrix) *\
            self.learning_rate
        ih_delta = bias_h_delta * input_matrix.transpose()

        # ADD DELTA
        # add delta to the weightHO
        self.w_ho += ho_delta

        # add delta to the weightIH
        self.w_ih += ih_delta

        # add bias delta
        self.bias_o += bias_o_delta
        self.bias_h += bias_h_delta

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-x))

    def desigmoid(self, x):
        vec = np.vectorize(lambda y: y * (1 - y))
        return vec(x)

    # NERUALEVOLUTION
    def mutate(self):
        self.w_ho = self.mutate_matrix(self.w_ho)
        self.w_ih = self.mutate_matrix(self.w_ih)
        self.bias_h = self.mutate_matrix(self.bias_h)
        self.bias_o = self.mutate_matrix(self.bias_o)

    def mutate_matrix(self, m):
        for i in range(len(m)):
            for j in range(len(m[i])):
                r = random()
                if r < self.mutate_rate:
                    m[i][j] += gauss(0, 0.1)
                elif r < self.mutate_rate * 2:
                    m[i][j] *= (random() + 1)
                elif r < self.mutate_rate * 3:
                    m[i][j] *= random()

        return m

    def copy(self):
        return NeuralNetWork(self, None, None)

    def crossover(self, other):
        child = self.copy()
        weights = [child.w_ho, child.w_ih, child.bias_h, child.bias_o]
        o_w = [other.w_ho, other.w_ih, other.bias_h, other.bias_o]
        for k, w in enumerate(weights):
            for i in range(len(w)):
                for j in range(len(w[i])):
                    r = random()
                    if r < 0.01:
                        w[i][j] = o_w[k][i][j]
        return child


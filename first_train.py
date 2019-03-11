import numpy as np
from train10 import train
import random

matrix = [0 for i in range(140)]

class Analyzer():

	def __init__(self, epochs):
		self.weights_0_1 = np.loadtxt('weights.txt')
		self.sigmoid_mapper = np.vectorize(self.sigmoid)
		# self.learning_rate = np.array([learning_rate])
		self.epochs = epochs

	def sigmoid(self, x):
		return 1/(1 + np.exp(-x))

	def predict(self, inputs):
		maxim = 0
		n = 0
		inputs_1 = np.dot(self.weights_0_1, inputs)
		outputs_1 = self.sigmoid_mapper(inputs_1)
		for i in outputs_1:
			if(i>maxim):
				maxim = i
				letter_number = n
			n+=1
		return letter_number

	def train_network(self, inputs, expected_predict):
		self.learning_rate = np.array([random.uniform(0.02, 0.09)])

		inputs_1 = np.dot(self.weights_0_1, inputs)
		outputs_1 = self.sigmoid_mapper(inputs_1)

		actual_predict = outputs_1

		error_layer_1 = np.array([actual_predict - expected_predict])
		gradient_layer_1 = outputs_1*(1 - outputs_1)
		weights_delta_layer_1 = error_layer_1*gradient_layer_1
		self.weights_0_1 -= (np.dot(inputs.reshape(len(inputs), 1), weights_delta_layer_1).T)*self.learning_rate

	def train(self):
		right_answers = 0
		count_of_answers = 0
		for i in range(self.epochs):
			inputs_ = []
			correct_predictions = []
			for input_stat, correct_predict in train:
				train_network.train_network(np.array(input_stat), correct_predict)
				inputs_.append(np.array(input_stat))
				correct_predictions.append(np.array(correct_predict))

				for j in range(len(correct_predict)):
					if(correct_predict[j] == 1 and train_network.predict(input_stat) == j):
						right_answers += 1
						# print(j)
				count_of_answers += 1
			if(((i/epochs)*100)%1 == 0 and ((i/epochs)*100)%5 == 0):
				print('Progress: ' + str(int((i/epochs)*100)) + '%')
				print('Train loss: ' + str(round(((count_of_answers-right_answers)/count_of_answers)*100, 2)) + '%')
				print('Wrong answers: ' + str(count_of_answers-right_answers))
				print('Quantity of answers: ' + str(count_of_answers) + '\n')
				right_answers = 0
				count_of_answers = 0

	def update_weights(self):
		np.savetxt('weights.txt', self.weights_0_1)

epochs = 1000
# learning_rate = 0.07
train_network = Analyzer(epochs = epochs)

train_network.train()
train_network.update_weights()
import numpy as np
import pygame
import math
from train_network import train_network

pygame.init()

counter = 26
mouse_down = False
mouse_down_right = False
keep_going = True
matrix = [0 for i in range(140)]
font = pygame.font.Font("CHILLER.TTF", 24)

class Analyzer():

	def __init__(self, learning_rate):
		self.weights_0_1 = np.loadtxt('weights.txt')
		self.sigmoid_mapper = np.vectorize(self.sigmoid)
		self.learning_rate = np.array([learning_rate])

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
		return chr(65+letter_number)

	def return_weights(self):
		return self.weights_0_1

class Update_matrix():

	def read_train():
		a =  open('train.py')
		counter = 0
		for i in a.read():
			counter += 1

		return counter

	def add_matrix_to_train(n, matrix, letter):
		num = ord(letter.upper())-65
		matrix_of_letter = [0]*26
		a = open('train.py')
		file_with_matrix = a.read(n-1)
		file_with_matrix += '\n\n		([  '
		for i in range(len(matrix)):
			if(i == len(matrix)-1):
				file_with_matrix += str(matrix[i])+'],\n\n		   ['
			else:
				file_with_matrix += str(matrix[i])+', '
			if((i+1)%10==0 and (i+1)!=len(matrix)):
				file_with_matrix += '\n			'

		for i in range(26):
			if(i == num):
				matrix_of_letter[i] = 1
		for i in range(len(matrix_of_letter)):
			if(i == len(matrix_of_letter)-1):
				file_with_matrix += str(matrix_of_letter[i])+']),]'
			else:
				file_with_matrix += str(matrix_of_letter[i])+', '
			if((i+1)%13==0 and (i+1)!=len(matrix_of_letter)):
				file_with_matrix += '\n			'	
		return file_with_matrix

	def rewrite_train(str_of_matrix):
		a = open('train.py', 'w')
		a.write(str_of_matrix)

	def read_new_train():
		a =  open('new_train.py')
		counter = 0
		for i in a.read():
			counter += 1

		return counter

	def add_matrix_to_new_train(n, matrix, letter):
		num = ord(letter.upper())-65
		matrix_of_letter = [0]*26
		a = open('new_train.py')
		if(n<20):
			file_with_matrix = a.read(n-1)
			file_with_matrix += 'new_train=[(['
		else:
			file_with_matrix = a.read(n-1)
			file_with_matrix += '\n\n		([  '
		for i in range(len(matrix)):
			if(i == len(matrix)-1):
				file_with_matrix += str(matrix[i])+'],\n\n		   ['
			else:
				file_with_matrix += str(matrix[i])+', '
			if((i+1)%10==0 and (i+1)!=len(matrix)):
				file_with_matrix += '\n			'

		for i in range(26):
			if(i == num):
				matrix_of_letter[i] = 1
		for i in range(len(matrix_of_letter)):
			if(i == len(matrix_of_letter)-1):
				file_with_matrix += str(matrix_of_letter[i])+']),]'
			else:
				file_with_matrix += str(matrix_of_letter[i])+', '
			if((i+1)%13==0 and (i+1)!=len(matrix_of_letter)):
				file_with_matrix += '\n			'	
		return file_with_matrix

	def rewrite_new_train(str_of_matrix):
		a = open('new_train.py', 'w')
		a.write(str_of_matrix)

	def check_answer():
		ask = input('Is it right?[y/n]').lower()
		if(ask == 'y'):
			print('its fine')
		elif(ask == 'n'):
			correct_letter = input('Please, write correct letter ')
			Update_matrix.rewrite_train(Update_matrix.add_matrix_to_train(Update_matrix.read_train(), matrix, correct_letter))
			Update_matrix.rewrite_new_train(Update_matrix.add_matrix_to_new_train(Update_matrix.read_new_train(), matrix, correct_letter))
			print('letter added\n')
		else: Update_matrix.check_answer()


class Draw():

	# def help_letter():
	# 	text = font.render('press ESC to end drawing', True, (255,255,255))
	# 	screen.blit(text,[310, 476])

	def draw(screen, x, y):
		pygame.draw.circle(screen, (255,255,255), (x, y), 5)

	def delete(screen, x ,y):
		pygame.draw.circle(screen, (0,0,0), (x, y), 20)

	def clear(screen):
		screen.fill((0,0,0))

	def get_border():
		min_x = 500
		max_x = 0
		min_y = 500
		max_y = 0
		for y in range(500):
			for x in range(500): 
				if(screen.get_at((x, y)) == (255,255,255,255)):
					if(x < min_x):
						min_x = x
					if(x > max_x):
						max_x = x
					if(y < min_y):
						min_y = y
					if(y > max_y):
						max_y = y
		return min_x, max_x, min_y, max_y

	def get_matrix(min_x, max_x, min_y, max_y, matrix):
		step_x = math.ceil((max_x - min_x)/10)
		step_y = math.ceil((max_y - min_y)/14)
		for i in range(14):
			for j in range(10):
				if(Draw.check_cell(min_x + step_x*j, min_y + step_y*i, step_x, step_y) == True):
					matrix[i*10+j] = 1
				else: matrix[i*10+j] = 0

	def check_cell(x, y, step_x, step_y):
		for i in range(step_y):
			for j in range(step_x):
				if(screen.get_at((x + j, y + i)) == (255,255,255,255)):
					return True
		return False

	def get_letter(matrix):
		num = network.predict(np.array(np.ravel(matrix)))
		return 'Your letter is ' + num + '\n'


learning_rate = 0.05
network = Analyzer(learning_rate = learning_rate)

a = open('new_train.py', 'w')
a.close()

print('\n\nLets draw letter')
screen = pygame.display.set_mode([500, 500])

while keep_going:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			keep_going = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				keep_going = False
			if(event.key == pygame.K_a):
				min_x, max_x, min_y, max_y = Draw.get_border()
				Draw.get_matrix(min_x, max_x, min_y, max_y, matrix)
				print(Draw.get_letter(matrix))
				Update_matrix.check_answer()
			if(event.key == pygame.K_c):
				Draw.clear(screen)
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_down = True
		if event.type == pygame.MOUSEBUTTONUP:
			mouse_down = False			
		if(event.type == pygame.MOUSEBUTTONDOWN):
			if(event.button == 3):
				mouse_down_right = True
		if(event.type == pygame.MOUSEBUTTONUP):
			if(event.button == 3):
				mouse_down_right = False			

	if(mouse_down):
		(mx, my) = pygame.mouse.get_pos()
		Draw.draw(screen, mx, my)
	if(mouse_down_right):
		(mx, my) = pygame.mouse.get_pos()
		Draw.delete(screen, mx, my)

	pygame.display.flip()
	# Draw.help_letter()

train_network.train()
train_network.update_weights()

pygame.quit()
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.callbacks import TensorBoard
import numpy as np
import os
import random

model = Sequential()

model.add(Conv2D(32, (3, 3), padding='same',
				input_shape=(176, 200, 3),
				activation='relu'))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Conv2D(64, (3, 3), padding='same',
				activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Conv2D(128, (3, 3), padding='same',
				activation='relu'))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(4, activation='softmax'))

learning_rate = 0.0001
opt = keras.optimizers.adam(lr=learning_rate, decay=1e-6)

model.compile(loss='categorical_crossentropy',
			optimizer=opt,
			metrics=['accuracy'])

tensorboard = TensorBoard(log_dir="logs/stage1")

train_data_dir = "train_data"



def check_data():
	choices = {"no_attacks": no_attacks,
			   "attack_closest_to_nexus": attack_closest_to_nexus,
			   "attack_enemy_structures": attack_enemy_structures,
			   "attack_enemy_start": attack_enemy_start}

	total_data = 0

	lengths = []
	for choice in choices:
		print("Length of {} is: {}".format(choice, len(choices[choice])))
		total_data += len(choices[choice])
		lengths.append(len(choices[choice]))

	print("Total data length now is:", total_data)
	return lengths
	
hm_epochs =10

for i in range(hm_epochs):
	current = 0
	increment = 200
	not_max = True
	all_files = os.listdir(train_data_dir)
	maximum = len(all_files)
	random.shuffle(all_files)

	while not_maximum:
		print("Currrently doing {}:{}".format(current, current+increment))
		no_attacks = []
		attack_closest_to_nexus = []
		attack_enemy_structures = []
		attack_enemy_start = []
		for file in all_files[current: current + increment]:
			full_path = os.path.join(train_data_dir, file)
			data = np.load(full_path)
			data = list(data)
			for d in data:
				choice = np.argmax(d[0])
				if choice == 0:
					no_attacks.append(d)
				elif choice == 1:
					attack_closest_to_nexus.append(d)
				elif choice == 2:
					attack_enemy_structures.append(d)
				elif choice == 2:
					attack_enemy_start.append(d)

		lengths = check_data()
		lowest_data = min(lengths)

		random.shuffle(no_attacks)
		random.shuffle(attack_enemy_start)
		random.shuffle(attack_enemy_structures)
		random.shuffle(attack_closest_to_nexus)

		no_attacks = no_attacks[:lowest_data]
		attack_enemy_start = attack_enemy_start[:lowest_data]
		attack_enemy_structures = attack_enemy_structures[:lowest_data]
		attack_closest_to_nexus = attack_closest_to_nexus[:lowest_data]

		check_data()
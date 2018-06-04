from utils_handouts import *
import numpy as np
import random



images, fine_labels  =   load_cifar100_data('cifar100/train')

print(images.shape)

sample = 100; # collect sample
tr = "tr" # use to assign name to sampled data
for i in range(0, 100):
	images_ = random.sample(population=list(images), k=sample);
	images_ = np.array(images_);
	# print (images_[1].shape)

	np.save('trainset/' + tr + str(i) + '.npy' , images_);















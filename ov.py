import numpy as np
import matplotlib.pyplot as plt
import random 

SIZE=10000


def ov(ass, bss):
	a = np.zeros(SIZE)
	b = np.zeros(SIZE)

	a[0: int(ass*SIZE)] = 1
	b[0: int(bss*SIZE)] = 1

	s =0
	for i in xrange(1000):
		np.random.shuffle(a)
		np.random.shuffle(b)
		s += np.sum(np.multiply(a,b)) / float(SIZE)

	print ("a=" ,ass, " b=", bss, "ov=", s/1000.)


ov(.27, .43)
ov(.43, .43)
ov(.27, .27)
ov(.3556, .3556)


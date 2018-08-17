import numpy as np
import matplotlib.pyplot as plt
import mpld3

V = np.array([[1,1],[-2,2],[4,-7]])
origin = [0], [0] # origin point

plt.quiver(*origin, V[:,0], V[:,1], color=['r','b','g'], scale=21)
mpld3.show()

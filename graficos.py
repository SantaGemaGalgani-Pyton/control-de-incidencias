import matplotlib.pyplot as plt
import numpy as np

def GraficoLineal():
    xpoints = np.array([0, 6])
    ypoints = np.array([0, 250])

    plt.plot(xpoints, ypoints)
    plt.show()
    pass

fig, ax = plt.subplots()            # Create a Figure and one Axes
ax.plot([1,2,3,4,5,6,7], [8,5,2,1,0,9,2])  # Plot some data on that Axes
plt.show()                           # Display the figure
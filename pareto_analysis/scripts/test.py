import matplotlib.pyplot as plt

plt.rcParams['mathtext.fontset'] = 'cm'
plt.plot([1, 2, 3], [4, 5, 6])
plt.xlabel(r"$x$")
plt.ylabel(r"$y$")
plt.tight_layout()
plt.show()

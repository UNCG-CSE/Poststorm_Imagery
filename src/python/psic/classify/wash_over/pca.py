import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

from psic.classify.wash_over.prepare_washover import get_washover_data

X, y = get_washover_data()

print('Calculating variances and information...')
pca = PCA().fit(X)

plt.figure(figsize=(8, 6))
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('# of Components')
plt.ylabel('Cumulative Explained Variance')
plt.grid(True)
plt.minorticks_on()
plt.show()

print('Plotting n = 2 principal component analysis...')
pca2 = PCA(n_components=2)
pca2.fit(X)
x_3d = pca2.transform(X)

plt.figure(figsize=(8, 6))
plt.scatter(x_3d[:, 0], x_3d[:, 1], c=y, alpha=0.5)
plt.ylabel('Principal Component 1')
plt.xlabel('Principal Component 2')
plt.show()

import warnings

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

from psic.classify.wash_over.prepare_washover import get_washover_data

warnings.filterwarnings("ignore")

SEED = 405

X, y = get_washover_data()

# print('Scaling the values for easier bounding...')
# scaler = StandardScaler()
# X = scaler.fit_transform(X)

print('Calculating variances and information...')
pca = PCA()
pca.fit_transform(X)
pca_variance = pca.explained_variance_

plt.figure(figsize=(8, 6))
plt.bar(range(len(X)), pca_variance, alpha=0.5, align='center', label='individual variance')
plt.legend()
plt.ylabel('Variance Ratio')
plt.xlabel('Principal Components')
plt.show()

pca2 = PCA(n_components=2)
pca2.fit(X)
x_3d = pca2.transform(X)

plt.figure(figsize=(8, 6))
plt.scatter(x_3d[:, 0], x_3d[:, 1], c=y, alpha=0.5)
plt.legend()
plt.ylabel('Principal Component 1')
plt.xlabel('Principal Component 2')
plt.show()
